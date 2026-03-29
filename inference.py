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

    "build_argument": """You are a senior litigation attorney. Study the available_precedents 
carefully. Pick the ONE most legally relevant precedent.
Respond ONLY with this exact JSON format, no markdown, no backticks:
{"point_1": "first argument point", "point_2": "second argument point", 
"point_3": "third argument point", "precedent_used": "exact precedent name from the list"}

The precedent_used field must be copied EXACTLY from the 
available_precedents list provided to you.""",

    "cross_examine": """You are a sharp cross-examination attorney.
Your goal is to expose contradictions in the witness statement.
Ask ONE specific, targeted question per turn.
Focus on timeline inconsistencies, distance/location conflicts, 
or factual contradictions.
Respond with ONLY the question, nothing else."""
}

def run_task(env, task_id, case_id=None, verbose=True):
    obs = env.reset(task_id=task_id, case_id=case_id)
    
    if task_id == "build_argument" and verbose:
        prec_names = [p["name"] for p in obs.content.get("available_precedents", [])]
        print(f"  [DEBUG] Case Precedents (Expected names): {prec_names}")

    final_score = 0.0
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
            
            # Precedent extraction fallback
            if not answer.get("precedent_used"):
                p1_words = re.findall(r'\w+', answer.get("point_1", "").lower())
                all_prec_words = set()
                for p in obs.content.get("available_precedents", []):
                    all_prec_words.update(re.findall(r'\w+', p["name"].lower()))
                
                for word in p1_words:
                    if word in all_prec_words:
                        answer["precedent_used"] = word
                        break
            
            if verbose:
                print(f"  [DEBUG] Parsed Answer: {answer}")
        else:
            answer = raw_answer
        
        action = Action(task_id=task_id, answer=answer)
        obs, reward, done, info = env.step(action)
        
        # Aggregation logic: Use MAX reward for all tasks
        final_score = max(final_score, reward.value)
        
        if verbose:
            print(f"  Turn {turn}: reward={reward.value:.2f} | "
                  f"info={reward.info}")
        
        if done:
            break
            
    return final_score

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
