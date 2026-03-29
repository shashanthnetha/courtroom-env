import json

def shares_words(s1: str, s2: str) -> bool:
    """Returns True if s1 and s2 share any word (case-insensitive)."""
    words1 = set(s1.lower().split())
    words2 = set(s2.lower().split())
    return not words1.isdisjoint(words2)

def grade_fallacy_identification(agent_answer: str, case: dict) -> float:
    if not isinstance(agent_answer, str):
        return 0.0
    normalized = agent_answer.lower().strip().replace(" ", "_")
    target = case["fallacy_type"].lower().strip().replace(" ", "_")
    if normalized == target:
        return 1.0
    if target in normalized:
        return 0.3
    return 0.0

def grade_argument_construction(agent_answer: dict, case: dict) -> float:
    """
    Bug 1 fix: Reward any point that is a non-empty string with > 5 words.
    Max score: 0.30 (precedent) + 0.60 (points) = 0.90, clamped to 1.0.
    """
    if not isinstance(agent_answer, dict):
        return 0.0
    
    score = 0.0
    precedent_used = agent_answer.get("precedent_used", "")
    
    relevant_precedent = next((p["name"] for p in case["precedents"] if p["relevant"]), None)
    red_herrings = [p["name"] for p in case["precedents"] if not p["relevant"]]
    
    if relevant_precedent and shares_words(precedent_used, relevant_precedent):
        score += 0.30
    else:
        for rh in red_herrings:
            if shares_words(precedent_used, rh):
                score -= 0.20
                break
        
    for i in range(3):
        point_key = f"point_{i+1}"
        point_text = agent_answer.get(point_key, "")
        if isinstance(point_text, str) and len(point_text.split()) > 5:
            score += 0.20
                
    return max(0.0, min(1.0, score))

def grade_cross_examination(current_question: str, case: dict, already_exposed: set) -> float:
    """
    Bug 2 fix: Only reward contradictions not already in already_exposed.
    """
    if not isinstance(current_question, str):
        return 0.0
    
    score = 0.0
    q_lower = current_question.lower()
    
    for i, contradiction in enumerate(case["contradictions"]):
        if i in already_exposed:
            continue
            
        triggers = [t.lower() for t in contradiction["trigger_keywords"]]
        if any(t in q_lower for t in triggers):
            score += 0.50
            
    return score

def compute_shaped_reward(
    task_id: str,
    agent_action: dict,
    case: dict,
    attempt_number: int,
    previous_actions: list,
    already_exposed: set = None
) -> tuple[float, dict]:
    base_score = 0.0
    loop_penalty = 0.0
    hallucination_penalty = 0.0
    structure_bonus = 0.0
    bugs_found = 0
    
    answer = agent_action.get("answer")
    
    if task_id == "identify_fallacy":
        base_score = grade_fallacy_identification(answer, case)
    elif task_id == "build_argument":
        base_score = grade_argument_construction(answer, case)
    elif task_id == "cross_examine":
        # Pass the set of already exposed indices to the grader
        base_score = grade_cross_examination(answer, case, already_exposed or set())
        
        # Calculate total unique bugs found across all turns for info dict
        all_questions = [a.get("answer") for a in previous_actions] + [answer]
        all_questions = [q for q in all_questions if isinstance(q, str)]
        for i, contradiction in enumerate(case["contradictions"]):
            triggers = [t.lower() for t in contradiction["trigger_keywords"]]
            if any(any(t in q.lower() for t in triggers) for q in all_questions):
                bugs_found += 1
                
    if attempt_number > 1:
        for prev in previous_actions:
            if answer == prev.get("answer"):
                loop_penalty = 0.10
                break
                
    if task_id == "build_argument" and isinstance(answer, dict):
        precedent_used = answer.get("precedent_used", "")
        if precedent_used:
            known_precedents = [p["name"] for p in case["precedents"]]
            is_hallucinated = True
            for known in known_precedents:
                if shares_words(precedent_used, known):
                    is_hallucinated = False
                    break
            if is_hallucinated:
                hallucination_penalty = 0.20
            
    if base_score == 0.0:
        if task_id == "build_argument":
            if isinstance(answer, dict) and all(k in answer for k in ["point_1", "point_2", "point_3", "precedent_used"]):
                structure_bonus = 0.05
        elif task_id in ["identify_fallacy", "cross_examine"]:
            if isinstance(answer, str) and len(answer) > 0:
                structure_bonus = 0.05
                
    final_reward = base_score - loop_penalty - hallucination_penalty + structure_bonus
    final_reward = max(0.0, min(1.0, final_reward))
    
    info = {
        "base_score": float(base_score),
        "loop_penalty": float(loop_penalty),
        "hallucination_penalty": float(hallucination_penalty),
        "structure_bonus": float(structure_bonus),
        "final_reward": float(final_reward),
        "bugs_found": int(bugs_found)
    }
    
    return final_reward, info
