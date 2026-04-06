import gradio as gr
from server.email_env_environment import EmailEnvironment
from models import Action

# 🌍 INIT ENV
env = EmailEnvironment(task="easy")
obs = env.reset()

score = 0
steps = 0


# 🧠 SMART AI (rule-based)
def smart_ai(email):
    email = email.lower()

    spam_keywords = [
        "free", "win", "winner", "prize", "cash",
        "urgent", "claim", "offer", "click", "buy"
    ]

    has_link = "http" in email or "www" in email

    score = 0

    for word in spam_keywords:
        if word in email:
            score += 1

    if has_link:
        score += 1

    return "spam" if score >= 1 else "not_spam"


# 🧠 EXPLAIN WHY
def explain_email(email):
    email = email.lower()

    reasons = []

    spam_keywords = [
        "free", "win", "winner", "prize", "cash",
        "urgent", "claim", "offer", "click", "buy"
    ]

    for word in spam_keywords:
        if word in email:
            reasons.append(f"keyword detected: '{word}'")

    if "http" in email or "www" in email:
        reasons.append("contains link")

    if not reasons:
        reasons.append("no strong spam signals")

    return reasons


# 👤 MANUAL CLASSIFICATION (with explanation)
def classify(action):
    global obs, score, steps

    current_email = obs.email_text
    reasons = explain_email(current_email)

    obs, reward, done, _ = env.step(Action(action_type=action))

    score += reward.value
    steps += 1

    avg = score / steps if steps > 0 else 0

    reason_text = "\n".join([f"- {r}" for r in reasons])

    return current_email, f"{reward.value} ({reward.reason})\n{reason_text}", f"{avg:.2f}"


# 🔄 CHANGE TASK
def change_task(task):
    global env, obs, score, steps

    env = EmailEnvironment(task=task)
    obs = env.reset()

    score = 0
    steps = 0

    return obs.email_text, "0", "0.0", ""


# 🤖 AUTO AI RUN (WITH EXPLANATION)
def run_ai():
    global env, obs, score, steps

    log = ""

    for _ in range(10):
        if env.done:
            break

        email = obs.email_text

        action = smart_ai(email)
        reasons = explain_email(email)

        obs, reward, done, _ = env.step(Action(action_type=action))

        score += reward.value
        steps += 1

        log += f"Step {steps}: {action} → {reward.value} ({reward.reason})\n"
        log += "Reason:\n"
        for r in reasons:
            log += f"  - {r}\n"
        log += "\n"

    avg = score / steps if steps > 0 else 0

    return obs.email_text, log, f"{avg:.2f}"


# 🎨 UI
with gr.Blocks() as demo:

    gr.Markdown("# 📧 AI Email Spam Detector")
    gr.Markdown("Play manually or run AI simulation with explainable decisions")

    # 🎯 Task selector
    task_selector = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Select Task"
    )

    # 📩 Email display
    email_box = gr.Textbox(label="📨 Email", lines=5)

    # 📊 Metrics
    reward_box = gr.Textbox(label="Reward + Explanation")
    score_box = gr.Textbox(label="Average Score")

    # 👤 Manual buttons
    spam_btn = gr.Button("🚨 Spam")
    not_spam_btn = gr.Button("✅ Not Spam")

    # 🤖 AI section
    gr.Markdown("## 🤖 Auto AI Simulation")
    ai_btn = gr.Button("Run AI Simulation")
    ai_log = gr.Textbox(label="AI Log + Explanation", lines=10)

    # 🔁 TASK CHANGE
    task_selector.change(
        change_task,
        inputs=task_selector,
        outputs=[email_box, reward_box, score_box, ai_log]
    )

    # 👤 MANUAL ACTIONS
    spam_btn.click(
        lambda: classify("spam"),
        outputs=[email_box, reward_box, score_box]
    )

    not_spam_btn.click(
        lambda: classify("not_spam"),
        outputs=[email_box, reward_box, score_box]
    )

    # 🤖 AI RUN
    ai_btn.click(
        fn=run_ai,
        outputs=[email_box, ai_log, score_box]
    )

# 🚀 LAUNCH
demo.launch()