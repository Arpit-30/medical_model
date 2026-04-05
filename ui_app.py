import gradio as gr
from server.email_env_environment import EmailEnvironment
from models import Action

env = EmailEnvironment(task="easy")
obs = env.reset()

score = 0
steps = 0


def classify(action):
    global obs, score, steps

    current_email = obs.email_text

    obs, reward, done, _ = env.step(Action(action_type=action))

    score += reward.value
    steps += 1

    avg = score / steps if steps > 0 else 0

    return current_email, f"{reward.value} ({reward.reason})", f"{avg:.2f}"


def change_task(task):
    global env, obs, score, steps

    env = EmailEnvironment(task=task)
    obs = env.reset()

    score = 0
    steps = 0

    return obs.email_text, "0", "0.0"


with gr.Blocks() as demo:

    gr.Markdown("# 📧 AI Email Spam Detector")
    gr.Markdown("Select task and classify emails like a real AI agent")

    task_selector = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Select Task"
    )

    email_box = gr.Textbox(label="📨 Email", lines=5)
    reward_box = gr.Textbox(label="Reward")
    score_box = gr.Textbox(label="Average Score")

    spam_btn = gr.Button("🚨 Spam")
    not_spam_btn = gr.Button("✅ Not Spam")

    task_selector.change(
        change_task,
        inputs=task_selector,
        outputs=[email_box, reward_box, score_box]
    )

    spam_btn.click(
        lambda: classify("spam"),
        outputs=[email_box, reward_box, score_box]
    )

    not_spam_btn.click(
        lambda: classify("not_spam"),
        outputs=[email_box, reward_box, score_box]
    )

demo.launch()