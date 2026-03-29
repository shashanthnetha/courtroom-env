from pydantic import BaseModel, Field
from typing import Any, Optional
import random
from .cases import CASES
from .tasks import IdentifyFallacyTask, BuildArgumentTask, CrossExamineTask
from .graders import compute_shaped_reward

class Observation(BaseModel):
    task_id: str
    case_id: str
    content: dict[str, Any] = Field(description="task-specific observation fields")
    attempt_number: int
    max_attempts: int

class Action(BaseModel):
    task_id: str
    answer: Any = Field(description="str for easy/hard, dict for medium")

class Reward(BaseModel):
    value: float = Field(ge=0.0, le=1.0)
    partial_credit: float
    info: dict[str, Any]

class CourtroomEnv:
    def __init__(self):
        self.tasks = {
            "identify_fallacy": IdentifyFallacyTask(),
            "build_argument": BuildArgumentTask(),
            "cross_examine": CrossExamineTask()
        }
        self._state = {}
        self.reset_called = False
    
    def reset(self, task_id: str = "identify_fallacy", 
              case_id: Optional[str] = None) -> Observation:
        """
        Select case and initialize state.
        """
        if task_id not in self.tasks:
            task_id = "identify_fallacy"
            
        task = self.tasks[task_id]
        
        selected_case = None
        if case_id:
            selected_case = next((c for c in CASES if c["case_id"] == case_id), None)
        
        if not selected_case:
            # Filter by difficulty
            eligible_cases = [c for c in CASES if c["difficulty"] == task.difficulty]
            selected_case = random.choice(eligible_cases) if eligible_cases else CASES[0]
            
        self._state = {
            "task_id": task_id,
            "case_id": selected_case["case_id"],
            "case": selected_case,
            "attempt_number": 1,
            "done": False,
            "previous_actions": [],
            "questions_asked": [],  # for cross_examine
            "contradictions_exposed_indices": set(),  # for cross_examine
            "turn": 1,
            "total_reward": 0.0,
            "witness_response": ""
        }
        
        self.reset_called = True
        
        max_attempts = getattr(task, "max_attempts", getattr(task, "max_turns", 1))
        
        obs_content = {}
        if task_id == "cross_examine":
            obs_content = task.get_observation(selected_case, turn=1)
        else:
            obs_content = task.get_observation(selected_case, attempt=1)
            
        return Observation(
            task_id=task_id,
            case_id=selected_case["case_id"],
            content=obs_content,
            attempt_number=1,
            max_attempts=max_attempts
        )
    
    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict]:
        """
        Execute one step in the environment.
        """
        if not self.reset_called:
            raise ValueError("Environment must be reset before step()")
            
        if self._state["done"]:
            # Return current state if already done
            obs = self._get_current_observation()
            reward = Reward(value=0.0, partial_credit=0.0, info={"error": "already done"})
            return obs, reward, True, {}

        if action.task_id != self._state["task_id"]:
            raise ValueError(f"Action task_id {action.task_id} does not match current task {self._state['task_id']}")

        task_id = self._state["task_id"]
        case = self._state["case"]
        attempt_number = self._state["attempt_number"]
        previous_actions = self._state["previous_actions"]
        already_exposed = self._state.get("contradictions_exposed_indices", set())
        
        # 1. Compute Reward
        reward_val, info = compute_shaped_reward(
            task_id=task_id,
            agent_action={"answer": action.answer},
            case=case,
            attempt_number=attempt_number,
            previous_actions=previous_actions,
            already_exposed=already_exposed
        )
        
        # 2. Update state
        self._state["previous_actions"].append({"answer": action.answer})
        
        witness_response = ""
        if task_id == "cross_examine":
            self._state["questions_asked"].append(action.answer)
            witness_response = self._simulate_witness(action.answer)
            self._state["witness_response"] = witness_response
            self._state["turn"] += 1
            self._state["attempt_number"] += 1
        else:
            self._state["attempt_number"] += 1
            
        # 3. Determine done
        done = False
        max_attempts = getattr(self.tasks[task_id], "max_attempts", getattr(self.tasks[task_id], "max_turns", 1))
        
        if reward_val >= 0.9:
            done = True
        elif self._state["attempt_number"] > max_attempts:
            done = True
        elif task_id == "cross_examine":
            if len(self._state["contradictions_exposed_indices"]) >= 2:
                done = True
                
        self._state["done"] = done
        self._state["total_reward"] += reward_val  # Still useful for internal tracking, but Reward below is the step reward
        
        # 4. Prepare return values
        next_obs = self._get_current_observation()
        
        reward_obj = Reward(
            value=reward_val,  # Correct: this is the step reward
            partial_credit=info.get("base_score", 0.0),
            info=info
        )
        
        return next_obs, reward_obj, done, info

    def _get_current_observation(self) -> Observation:
        task_id = self._state["task_id"]
        task = self.tasks[task_id]
        case = self._state["case"]
        attempt = self._state["attempt_number"]
        max_attempts = getattr(task, "max_attempts", getattr(task, "max_turns", 1))
        
        if task_id == "cross_examine":
            obs_content = task.get_observation(
                case, 
                turn=self._state["turn"], 
                witness_response=self._state["witness_response"],
                contradictions_exposed=len(self._state["contradictions_exposed_indices"])
            )
        else:
            obs_content = task.get_observation(case, attempt=attempt)
            
        return Observation(
            task_id=task_id,
            case_id=case["case_id"],
            content=obs_content,
            attempt_number=min(attempt, max_attempts),
            max_attempts=max_attempts
        )

    def _simulate_witness(self, question: str) -> str:
        if not isinstance(question, str):
            return "I don't understand the question."
            
        case = self._state["case"]
        q_lower = question.lower()
        
        exposed_in_this_turn = False
        for i, contradiction in enumerate(case["contradictions"]):
            if i in self._state["contradictions_exposed_indices"]:
                continue
                
            triggers = [t.lower() for t in contradiction["trigger_keywords"]]
            if all(t in q_lower for t in triggers):
                self._state["contradictions_exposed_indices"].add(i)
                exposed_in_this_turn = True
                break
        
        if exposed_in_this_turn:
            return "Well... I mean, it was around that time, I think. Things were hectic."
        else:
            return "I've already told you everything I remember about that day."

    def state(self) -> dict:
        """Return current _state dict"""
        return self._state.copy()
