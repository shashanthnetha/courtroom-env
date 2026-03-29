---
title: Courtroom Env
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: gradio
pinned: false
---

# courtroom-env

courtroom-env is the first legal argumentation environment on OpenEnv. 
It benchmarks AI agent performance on three progressively harder legal 
reasoning tasks: logical fallacy detection, evidence-based argument 
construction, and multi-turn cross-examination. It directly measures 
hallucination resistance (agents are penalized for citing non-existent 
precedents), red-herring rejection, and multi-step deductive reasoning.

## Motivation
Legal reasoning represents one of the most challenging frontiers for Large Language Models (LLMs). Unlike general-purpose reasoning, legal tasks require high precision, strict adherence to precedents, and the ability to detect subtle inconsistencies in testimony. `courtroom-env` provides a structured playground for agents to practice and be benchmarked on these critical skills, addressing a significant gap in the OpenEnv Hub.

## Environment Overview
The environment simulates a courtroom setting where the agent acts as an attorney. It consists of 15 synthetic but realistic cases across various areas of law (criminal, tort, contract, property). Agents interact with the environment through tasks of increasing difficulty, receiving shaped rewards based on their performance and efficiency.

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| task_id | string | Identifier for the current task |
| case_id | string | Identifier for the current case |
| content | object | Task-specific data (facts, precedents, witness statements) |
| attempt_number | integer | Current attempt or turn number |
| max_attempts | integer | Maximum allowed attempts for the task |

## Action Space
| Field | Type | Description |
|-------|------|-------------|
| task_id | string | Must match the current task_id |
| answer | string / object | Fallacy type (str), question (str), or counter-argument (JSON) |

## Tasks

### Identify Fallacy
- **Description:** Detect the logical fallacy in the opposing counsel's argument.
- **Difficulty:** Easy
- **Success Criteria:** Exactly matching the fallacy type (e.g., `straw_man`).
- **Example:** Identifying a "slippery slope" argument in a criminal case.

### Build Argument
- **Description:** Construct a 3-point counter-argument using the correct legal precedent.
- **Difficulty:** Medium
- **Success Criteria:** Using the relevant precedent and addressing key points accurately.
- **Example:** Citing a specific tort law precedent to override a signed waiver.

### Cross-Examine
- **Description:** Question a witness to expose two subtle contradictions.
- **Difficulty:** Hard
- **Success Criteria:** Asking questions that contain specific keywords related to the contradictions.
- **Example:** Exposing a witness's inability to see a car clearly in the dark.

## Reward Function
The reward function is shaped to encourage precision and discourage common LLM failures:
- **Base Score:** Accuracy on the core task (0.0 - 1.0).
- **Loop Penalty:** -0.10 for repeating the same action.
- **Hallucination Penalty:** -0.20 for citing precedents not provided in the case.
- **Structure Bonus:** +0.05 for providing a valid response format even if the content is incorrect.
- **Efficiency Penalty:** -0.05 per extra question in cross-examination.

## Setup

### Local Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Docker
```bash
docker build -t courtroom-env .
docker run -p 7860:7860 courtroom-env
```

## Running Inference
The `inference.py` script provides a baseline agent implementation:
```bash
export HF_TOKEN="your_token_here"
python inference.py
```

## Baseline Scores
| Task | Score |
|------|-------|
| identify_fallacy | 0.85 |
| build_argument | 0.62 |
| cross_examine | 0.38 |

## Environment Variables
- `API_BASE_URL`: LLM endpoint (default: Hugging Face Router)
- `MODEL_NAME`: The model to benchmark (default: Llama-3.1-8B-Instruct)
- `HF_TOKEN`: Your API key for model access

## Project Structure
```
courtroom-env/
├── env/
│   ├── __init__.py
│   ├── environment.py   # Core logic
│   ├── tasks.py         # Task definitions
│   ├── graders.py       # Deterministic grading
│   └── cases.py         # 15 legal cases
├── app.py               # FastAPI wrapper
├── inference.py         # Baseline agent
├── openenv.yaml         # OpenEnv metadata
├── Dockerfile
├── requirements.txt
└── README.md
```
