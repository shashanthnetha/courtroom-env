"""
Inference Script — courtroom-env
Baseline agent using OpenAI client against all 3 tasks.

Environment variables:
  API_BASE_URL  - LLM endpoint (default: https://router.huggingface.co/v1)
  MODEL_NAME    - Model identifier
  HF_TOKEN      - API key
"""

import os, json, re
from openai import OpenAI
from env.environment import CourtroomEnv, Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

SYSTEM_PROMPTS = {
    "identify_fallacy": """You are an expert lawyer and logician. 
You will be given a legal case and an opposing argument.
Identify the logical fallacy. 
Respond with ONLY one of these exact strings, nothing else:
straw_man, ad_hominem, false_dichotomy, slippery_slope, appeal_to_authority""",

    "build_argument": """You are a senior litigation attorney.
Build a counter-argument using the most relevant legal precedent.
Respond ONLY with valid JSON in this exact format:
{"point_1": "...", "point_2": "...", "point_3": "...", "precedent_used": "..."}
No explanation. No markdown. Pure JSON only.""",

    "cross_examine": """You are a sharp cross-examination attorney.
Your goal is to expose contradictions in the witness statement.
Ask ONE specific, targeted question per turn.
Focus on timeline inconsistencies, distance/location conflicts, 
or factual contradictions.
Respond with ONLY the question, nothing else."""
}

def run_task(env, task_id, case_id=None, verbose=True):
    obs = env.reset(task_id=task_id, case_id=case_id)
    total_reward = 0.0
    done = False
    turn = 0
    
    while not done:
        turn += 1
        # Build user message from observation content
        user_msg = json.dumps(obs.content, indent=2)
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[task_id]},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.1,
                max_tokens=300
            )
            raw_answer = response.choices[0].message.content.strip()
        except Exception as e:
            if verbose:
                print(f"  Turn {turn}: API Error: {e}")
            # Use dummy answers to allow script to continue if API fails
            if task_id == "identify_fallacy": raw_answer = "straw_man"
            elif task_id == "build_argument": raw_answer = "{}"
            else: raw_answer = "When did you check the scaffold?"
        
        # Parse answer based on task
        if task_id == "build_argument":
            try:
                # Strip markdown backticks if present
                clean = re.sub(r'```json|```', '', raw_answer).strip()
                answer = json.loads(clean)
            except:
                answer = {"point_1": raw_answer, "point_2": "", 
                         "point_3": "", "precedent_used": ""}
        else:
            answer = raw_answer
        
        action = Action(task_id=task_id, answer=answer)
        obs, reward, done, info = env.step(action)
        total_reward += reward.value
        
        if verbose:
            print(f"  Turn {turn}: reward={reward.value:.2f} | "
                  f"info={reward.info}")
        
        if done:
            break
    
    return total_reward

def main():
    if API_KEY == "dummy":
        print("Warning: HF_TOKEN or API_KEY not set. Using dummy key. API calls will likely fail.")
        
    env = CourtroomEnv()
    results = {}
    
    tasks = ["identify_fallacy", "build_argument", "cross_examine"]
    
    for task_id in tasks:
        print(f"\n{'='*50}")
        print(f"Running task: {task_id}")
        print('='*50)
        score = run_task(env, task_id, verbose=True)
        results[task_id] = round(score, 4)
        print(f"Final score for {task_id}: {score:.4f}")
    
    print(f"\n{'='*50}")
    print("BASELINE RESULTS SUMMARY")
    print('='*50)
    for task_id, score in results.items():
        print(f"  {task_id}: {score:.4f}")
    
    avg = sum(results.values()) / len(results)
    print(f"  Average: {avg:.4f}")
    print('='*50)

if __name__ == "__main__":
    main()
