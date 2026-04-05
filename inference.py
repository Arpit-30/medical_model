import os
from openai import OpenAI
from server.email_env_environment import EmailEnvironment
from grader import EmailGrader
from models import Action

# ✅ Safe OpenAI initialization
use_api = False
client = None

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("API_BASE_URL")
model_name = os.getenv("MODEL_NAME")

if api_key:
    try:
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        use_api = True
    except Exception as e:
        print(f"[WARN] OpenAI init failed: {e}")
        use_api = False


# 🧠 Rule-based AI (fallback)
def smart_ai(email):
    email = email.lower()

    spam_keywords = [
        "free", "win", "winner", "prize", "cash",
        "urgent", "claim", "offer", "click", "buy"
    ]

    if any(word in email for word in spam_keywords):
        return "spam"
    return "not_spam"


# 🤖 OpenAI-based AI
def llm_ai(email):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": f"Classify this email as spam or not_spam.\nOnly reply: spam OR not_spam\n\nEmail:\n{email}"
            }]
        )

        output = response.choices[0].message.content.lower()

        if "spam" in output:
            return "spam"
        return "not_spam"

    except Exception as e:
        print(f"[WARN] API failed, switching to fallback: {e}")
        return smart_ai(email)


tasks = ["easy", "medium", "hard"]

print("[START]")

for task in tasks:
    print(f"\n--- Running Task: {task} ---")

    env = EmailEnvironment(task=task)
    grader = EmailGrader()

    obs = env.reset()
    done = False

    while not done:

        # 🔥 SAFE HYBRID LOGIC
        if use_api:
            action = llm_ai(obs.email_text)
        else:
            action = smart_ai(obs.email_text)

        # 🔍 True label BEFORE step
        true_label = env.df.iloc[env.index]['label']

        obs, reward, done, _ = env.step(Action(action_type=action))

        score = grader.grade(true_label, Action(action_type=action))

        # ✅ STRICT FORMAT (IMPORTANT)
        print(f"[STEP] task={task} action={action} reward={reward.value} score={score}")

    final_score = grader.final_score()
    print(f"[RESULT] task={task} score={final_score}")

print("[END]")