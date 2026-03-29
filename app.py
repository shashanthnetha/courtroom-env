from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
from env.environment import CourtroomEnv, Action, Observation

app = FastAPI(title="courtroom-env", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = CourtroomEnv()

class ResetRequest(BaseModel):
    task_id: str = "identify_fallacy"
    case_id: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok", "environment": "courtroom-env", "version": "1.0.0"}

@app.post("/reset")
async def reset(request: ResetRequest):
    try:
        obs = env.reset(task_id=request.task_id, case_id=request.case_id)
        return obs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step(action: Action):
    if not env.reset_called:
        raise HTTPException(status_code=400, detail="Environment must be reset before step()")
    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": info
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def get_state():
    return env.state()

@app.get("/tasks")
async def get_tasks():
    tasks_list = []
    for task_id, task in env.tasks.items():
        max_attempts = getattr(task, "max_attempts", getattr(task, "max_turns", 1))
        tasks_list.append({
            "id": task_id,
            "difficulty": task.difficulty,
            "description": task.description,
            "max_attempts": max_attempts
        })
    return tasks_list
