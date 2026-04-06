import gradio as gr
from server.email_env_environment import EmailEnvironment
from models import Action

env = None
obs = None
score = 0
steps = 0


# 🧠 AI MODEL
def smart_ai(email):
    email = email.lower()
    keywords = ["free", "win", "offer", "urgent", "cash"]

    score_val = sum(1 for w in keywords if w in email)
    if "http" in email or "www" in email:
        score_val += 1

    return "spam" if score_val >= 1 else "not_spam"


# 🧠 EXPLAINABILITY
def explain(email):
    email = email.lower()
    reasons = []

    for w in ["free", "win", "offer", "urgent", "cash"]:
        if w in email:
            reasons.append(f"keyword: {w}")

    if "http" in email or "www" in email:
        reasons.append("contains link")

    return ", ".join(reasons) if reasons else "no strong spam signals"


# 👤 MANUAL ACTION
def classify(action):
    global obs, score, steps

    if obs is None:
        return "⚠️ Please select a task first", "", ""

    email_text = obs.email_text
    reason = explain(email_text)

    obs, reward, done, _ = env.step(Action(action_type=action))

    score += reward.value
    steps += 1

    avg = score / steps if steps else 0

    return email_text, f"{reward.value} | {reason}", f"{avg:.2f}"


# 🔄 TASK CHANGE
def change_task(task):
    global env, obs, score, steps

    if task == "Select Task":
        return (
            "",
            "⚠️ Please select a task",
            "0.0",
            "",
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
        )

    env = EmailEnvironment(task=task)
    obs = env.reset()

    score = 0
    steps = 0

    return (
        obs.email_text,
        "0",
        "0.0",
        "",
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


# 🤖 AUTO AI
def run_ai():
    global env, obs, score, steps

    if obs is None:
        return "", "⚠️ Please select a task first", ""

    log_text = ""

    for _ in range(5):
        if env.done:
            break

        email_text = obs.email_text
        action = smart_ai(email_text)
        reason = explain(email_text)

        obs, reward, done, _ = env.step(Action(action_type=action))

        score += reward.value
        steps += 1

        log_text += f"Step {steps}: {action.upper()} → {reward.value}\n"
        log_text += f"   Reason: {reason}\n\n"

    avg = score / steps if steps else 0

    return obs.email_text, log_text, f"{avg:.2f}"


# 🎨 UI (MOBILE FRIENDLY + CLEAN)
with gr.Blocks(fill_width=True) as demo:

    gr.Markdown("## 📧 AI Email Spam Detector")
    gr.Markdown("Select a task → classify emails manually or run AI simulation")

    task = gr.Dropdown(
        ["Select Task", "easy", "medium", "hard"],
        value="Select Task",
        label="🎯 Select Task"
    )

    email = gr.Textbox(label="📨 Email", lines=3)

    reward = gr.Textbox(label="🎯 Reward + Explanation")

    score_box = gr.Textbox(label="📊 Average Score")

    spam = gr.Button("🚨 Mark as Spam", interactive=False)
    not_spam = gr.Button("✅ Mark as Safe", interactive=False)

    ai = gr.Button("🤖 Run AI Simulation", interactive=False)

    log = gr.Textbox(label="🤖 AI Decision Log", lines=5)

    # 🔁 TASK CHANGE
    task.change(
        change_task,
        inputs=task,
        outputs=[email, reward, score_box, log, spam, not_spam, ai]
    )

    # 👤 MANUAL ACTIONS
    spam.click(
        lambda: classify("spam"),
        outputs=[email, reward, score_box]
    )

    not_spam.click(
        lambda: classify("not_spam"),
        outputs=[email, reward, score_box]
    )

    # 🤖 AUTO AI
    ai.click(
        run_ai,
        outputs=[email, log, score_box]
    )


demo.launch()