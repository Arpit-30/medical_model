import pandas as pd
from models import Observation, Action, Reward


# 🔗 Detect links
def detect_link(text):
    return "http" in text or "www" in text


# 💰 Detect money / scam signals
def detect_money(text):
    text = text.lower()
    return "$" in text or "£" in text or "prize" in text or "cash" in text


# 🚨 Detect spam keywords
def has_spam_words(text):
    spam_keywords = ["free", "win", "offer", "urgent", "money"]
    return any(word in text.lower() for word in spam_keywords)


class EmailEnvironment:
    def __init__(self, task="easy"):
        df = pd.read_csv("data/emails_clean.csv", encoding="latin-1")

        # 🎯 TASK DIFFICULTY (IMPORTANT)
        if task == "easy":
            self.df = df.sample(frac=0.3, random_state=42)
        elif task == "medium":
            self.df = df.sample(frac=0.6, random_state=42)
        else:
            self.df = df

        self.index = 0
        self.done = False
        self.task = task

    def reset(self):
        self.index = 0
        self.done = False

        row = self.df.iloc[self.index]

        return Observation(
            email_text=row['text'],
            has_link=detect_link(row['text']),
            has_money=detect_money(row['text']),   # 🔥 NEW
            step_count=0
        )

    def step(self, action: Action):
        row = self.df.iloc[self.index]
        true_label = row['label']
        text = row['text']

        # 🔥 TASK LOGIC
        if self.task == "easy":
            correct = (action.action_type == true_label)

        elif self.task == "medium":
            # rule-based (link + spam words)
            if detect_link(text) or has_spam_words(text):
                correct = (action.action_type == "spam")
            else:
                correct = (action.action_type == "not_spam")

        elif self.task == "hard":
            # multi-signal scoring
            score = 0
            if detect_link(text):
                score += 1
            if has_spam_words(text):
                score += 1
            if detect_money(text):
                score += 1

            if score >= 1:
                correct = (action.action_type == "spam")
            else:
                correct = (action.action_type == "not_spam")

        # 🎯 REWARD SYSTEM (REALISTIC)
        if action.action_type == true_label:
            reward = Reward(value=1.0, reason="Correct")
        elif action.action_type == "spam" and true_label == "not_spam":
            reward = Reward(value=-1.0, reason="False Positive (bad UX)")
        else:
            reward = Reward(value=-0.5, reason="Missed Spam")

        # ⏳ Penalty for too many steps (lazy agent)
        if self.index > 50:
            reward = Reward(value=-0.2, reason="Too slow")
        # 👉 Move forward
        self.index += 1

        if self.index >= len(self.df):
            self.done = True

        # 🔁 Next observation
        if not self.done:
            next_row = self.df.iloc[self.index]
            next_obs = Observation(
                email_text=next_row['text'],
                has_link=detect_link(next_row['text']),
                has_money=detect_money(next_row['text']),  # 🔥 NEW
                step_count=self.index
            )
        else:
            next_obs = Observation(
                email_text="",
                has_link=False,
                has_money=False,
                step_count=self.index
            )

        return next_obs, reward, self.done, {}

    def state(self):
        return {
            "index": self.index,
            "task": self.task,
            "done": self.done
        }