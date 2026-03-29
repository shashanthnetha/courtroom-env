class IdentifyFallacyTask:
    task_id = "identify_fallacy"
    difficulty = "easy"
    max_attempts = 3
    description = "Identify the logical fallacy in the opposing counsel's argument"
    
    def get_observation(self, case: dict, attempt: int) -> dict:
        return {
            "task_id": self.task_id,
            "case_id": case["case_id"],
            "case_facts": case["facts"],
            "opposing_argument": case["opposing_argument"],
            "instructions": "Identify the logical fallacy. Respond with exactly one of: straw_man, ad_hominem, false_dichotomy, slippery_slope, appeal_to_authority",
            "attempt_number": attempt,
            "max_attempts": self.max_attempts
        }

class BuildArgumentTask:
    task_id = "build_argument"
    difficulty = "medium"
    max_attempts = 3
    description = "Construct a 3-point counter-argument using the relevant precedent"
    
    def get_observation(self, case: dict, attempt: int) -> dict:
        return {
            "task_id": self.task_id,
            "case_id": case["case_id"],
            "case_facts": case["facts"],
            "available_precedents": [
                {"name": p["name"], "summary": p["summary"]} 
                for p in case["precedents"]
            ],
            "instructions": "Build a counter-argument. Respond with JSON: {\"point_1\": str, \"point_2\": str, \"point_3\": str, \"precedent_used\": str}",
            "attempt_number": attempt,
            "max_attempts": self.max_attempts
        }

class CrossExamineTask:
    task_id = "cross_examine"
    difficulty = "hard"
    max_turns = 5
    description = "Cross-examine the witness to expose 2 contradictions in their statement"
    
    def get_observation(self, case: dict, turn: int, 
                        witness_response: str = "", contradictions_exposed: int = 0) -> dict:
        return {
            "task_id": self.task_id,
            "case_id": case["case_id"],
            "witness_statement": case["witness_statement"],
            "current_turn": turn,
            "max_turns": self.max_turns,
            "last_witness_response": witness_response,
            "instructions": "Ask ONE question to expose contradictions in the witness statement. Be specific.",
            "contradictions_exposed": contradictions_exposed
        }
