import gradio as gr
import json
from env.environment import CourtroomEnv, Action

env = CourtroomEnv()

def reset_env(task_id):
    obs = env.reset(task_id=task_id)
    return json.dumps(obs.model_dump(), indent=2)

def step_env(task_id, answer):
    try:
        action = Action(task_id=task_id, answer=answer)
        obs, reward, done, info = env.step(action)
        return json.dumps({
            "observation": obs.model_dump(),
            "reward": reward.model_dump(),
            "done": done,
            "info": info
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_state():
    return json.dumps(env.state(), indent=2, default=str)

with gr.Blocks(title="courtroom-env") as demo:
    gr.Markdown("# ⚖️ courtroom-env\nLegal argumentation environment for AI agents")
    
    with gr.Row():
        task_dropdown = gr.Dropdown(
            choices=["identify_fallacy", "build_argument", "cross_examine"],
            value="identify_fallacy",
            label="Task"
        )
        reset_btn = gr.Button("Reset", variant="primary")
    
    obs_output = gr.Textbox(label="Observation", lines=10)
    answer_input = gr.Textbox(label="Answer / Action", lines=3)
    step_btn = gr.Button("Step", variant="secondary")
    step_output = gr.Textbox(label="Result", lines=10)
    state_btn = gr.Button("Get State")
    state_output = gr.Textbox(label="State", lines=5)

    reset_btn.click(reset_env, inputs=[task_dropdown], outputs=[obs_output])
    step_btn.click(step_env, inputs=[task_dropdown, answer_input], outputs=[step_output])
    state_btn.click(get_state, outputs=[state_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
