import gradio as gr
from server.email_env_environment import EmailEnvironment
from models import Action

# 🌍 INIT
env = EmailEnvironment(task="easy")
obs = env.reset()

score = 0
steps = 0


# 🧠 AI
def smart_ai(email):
    email = email.lower()
    keywords = ["free", "win", "offer", "urgent", "cash"]

    score = sum(1 for w in keywords if w in email)
    if "http" in email or "www" in email:
        score += 1

    return "spam" if score >= 1 else "not_spam"


# 🧠 EXPLAIN
def explain(email):
    email = email.lower()
    reasons = []

    for w in ["free", "win", "offer", "urgent", "cash"]:
        if w in email:
            reasons.append(f"{w}")

    if "http" in email or "www" in email:
        reasons.append("link")

    return ", ".join(reasons) if reasons else "clean"


# 👤 MANUAL
def classify(action):
    global obs, score, steps

    email = obs.email_text
    reason = explain(email)

    obs, reward, done, _ = env.step(Action(action_type=action))

    score += reward.value
    steps += 1

    avg = score / steps if steps else 0

    return email, f"{reward.value} | {reason}", f"{avg:.2f}"


# 🔄 TASK
def change_task(task):
    global env, obs, score, steps

    env = EmailEnvironment(task=task)
    obs = env.reset()

    score = 0
    steps = 0

    return obs.email_text, "0", "0.0", ""


# 🤖 AUTO AI
def run_ai():
    global env, obs, score, steps

    log = ""

    for _ in range(5):  # small for mobile
        if env.done:
            break

        email = obs.email_text
        action = smart_ai(email)
        reason = explain(email)

        obs, reward, done, _ = env.step(Action(action_type=action))

        score += reward.value
        steps += 1

        log += f"{steps}: {action} ({reason}) → {reward.value}\n"

    avg = score / steps if steps else 0

    return obs.email_text, log, f"{avg:.2f}"


# 🎨 MOBILE UI
with gr.Blocks(fill_width=True) as demo:

    gr.Markdown("## 📧 Spam AI")

    task = gr.Dropdown(["easy", "medium", "hard"], value="easy")

    email = gr.Textbox(lines=3)
    reward = gr.Textbox()
    score_box = gr.Textbox()

    spam = gr.Button("Spam")
    not_spam = gr.Button("Not Spam")

    ai = gr.Button("Run AI")
    log = gr.Textbox(lines=4)

    task.change(change_task, task, [email, reward, score_box, log])

    spam.click(lambda: classify("spam"), outputs=[email, reward, score_box])
    not_spam.click(lambda: classify("not_spam"), outputs=[email, reward, score_box])

    ai.click(run_ai, outputs=[email, log, score_box])


demo.launch()