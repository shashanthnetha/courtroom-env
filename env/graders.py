import json

def grade_fallacy_identification(agent_answer: str, case: dict) -> float:
    """
    agent_answer: the fallacy type string the agent identified
    Returns: 1.0 if exact match with case["fallacy_type"]
             0.3 if agent answer contains the correct type as substring
             0.0 otherwise
    Normalize agent_answer: lowercase, strip whitespace, replace spaces with underscores
    """
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
    agent_answer: dict with keys "point_1", "point_2", "point_3", "precedent_used"
    
    Score breakdown:
    - precedent_used matches case's relevant precedent name: +0.30
    - each of 3 points contains at least 2 keywords from correct_argument_points[i]: +0.20 each (total 0.60)
    - penalty: if precedent_used matches a red herring: -0.20
    
    Clamp final score to [0.0, 1.0]
    """
    if not isinstance(agent_answer, dict):
        return 0.0
    
    score = 0.0
    precedent_used = agent_answer.get("precedent_used", "")
    
    # Precedent check
    relevant_precedent = next((p["name"] for p in case["precedents"] if p["relevant"]), None)
    red_herrings = [p["name"] for p in case["precedents"] if not p["relevant"]]
    
    if relevant_precedent and precedent_used == relevant_precedent:
        score += 0.30
    elif precedent_used in red_herrings:
        score -= 0.20
        
    # Points check
    for i in range(3):
        point_key = f"point_{i+1}"
        point_text = agent_answer.get(point_key, "").lower()
        correct_points = case["correct_argument_points"]
        
        if i < len(correct_points):
            # We use a simple keyword matching for the "points"
            # Since the prompt says "contains at least 2 keywords from correct_argument_points[i]"
            # But correct_argument_points[i] IS a string. 
            # I will split it into words and filter for common words to get "keywords"
            target_point = correct_points[i].lower()
            keywords = [w for w in target_point.split() if len(w) > 3]
            
            match_count = sum(1 for kw in keywords if kw in point_text)
            if match_count >= 2:
                score += 0.20
                
    return max(0.0, min(1.0, score))

def grade_cross_examination(questions_asked: list[str], case: dict) -> float:
    """
    questions_asked: list of question strings agent asked across all turns
    
    For each contradiction in case["contradictions"]:
        Check if any question in questions_asked contains ALL trigger_keywords (case-insensitive)
        If yes: this contradiction is "exposed" -> +0.50
    
    Deduct 0.05 for each question asked beyond the minimum needed (efficiency penalty, max deduction 0.15)
    
    Clamp to [0.0, 1.0]
    """
    score = 0.0
    exposed_count = 0
    
    for contradiction in case["contradictions"]:
        triggers = [t.lower() for t in contradiction["trigger_keywords"]]
        found = False
        for q in questions_asked:
            q_lower = q.lower()
            if all(t in q_lower for t in triggers):
                found = True
                break
        if found:
            exposed_count += 1
            score += 0.50
            
    # Efficiency penalty: minimum needed is 2 (one for each contradiction)
    # Deduct 0.05 for each beyond 2, max 0.15
    if len(questions_asked) > 2:
        penalty = (len(questions_asked) - 2) * 0.05
        score -= min(penalty, 0.15)
        
    return max(0.0, min(1.0, score))

def compute_shaped_reward(
    task_id: str,
    agent_action: dict,
    case: dict,
    attempt_number: int,
    previous_actions: list
) -> tuple[float, dict]:
    """
    Master reward function. Returns (reward_value, info_dict).
    """
    base_score = 0.0
    loop_penalty = 0.0
    hallucination_penalty = 0.0
    structure_bonus = 0.0
    bugs_found = 0
    
    # Base Score calculation
    answer = agent_action.get("answer")
    
    if task_id == "identify_fallacy":
        base_score = grade_fallacy_identification(answer, case)
    elif task_id == "build_argument":
        base_score = grade_argument_construction(answer, case)
    elif task_id == "cross_examine":
        # For cross_examine, the 'answer' is the current question
        # But we need the history. We assume previous_actions contains the history.
        questions = [a.get("answer") for a in previous_actions] + [answer]
        questions = [q for q in questions if isinstance(q, str)]
        base_score = grade_cross_examination(questions, case)
        
        # Count bugs found for info dict
        for contradiction in case["contradictions"]:
            triggers = [t.lower() for t in contradiction["trigger_keywords"]]
            if any(all(t in q.lower() for t in triggers) for q in questions if isinstance(q, str)):
                bugs_found += 1
                
    # Loop penalty
    if attempt_number > 1:
        for prev in previous_actions:
            if answer == prev.get("answer"):
                loop_penalty = 0.10
                break
                
    # Hallucination penalty (for build_argument)
    if task_id == "build_argument" and isinstance(answer, dict):
        precedent_used = answer.get("precedent_used", "")
        known_precedents = [p["name"] for p in case["precedents"]]
        if precedent_used and precedent_used not in known_precedents:
            hallucination_penalty = 0.20
            
    # Structure bonus
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
