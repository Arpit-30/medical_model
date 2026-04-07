import pandas as pd
from models import Observation, Action, Reward


class MedicalEnvironment:
    def __init__(self, task="easy"):
        df = pd.read_csv("data/triage.csv")

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
            symptoms=row["text"],
            step_count=0
        )

    def step(self, action: Action):
        row = self.df.iloc[self.index]
        true_label = row["label"]

        # 🎯 TASK LOGIC
        if action.action_type == true_label:
            reward = Reward(value=1.0, reason="Correct")
        elif action.action_type == "not_urgent" and true_label == "urgent":
            reward = Reward(value=-1.0, reason="Missed urgent case")
        else:
            reward = Reward(value=-0.5, reason="False alarm")

        # move forward
        self.index += 1

        if self.index >= len(self.df):
            self.done = True

        # next observation
        if not self.done:
            next_row = self.df.iloc[self.index]
            obs = Observation(
                symptoms=next_row["text"],
                step_count=self.index
            )
        else:
            obs = Observation(symptoms="", step_count=self.index)

        return obs, reward, self.done, {}

    def state(self):
        return {
            "index": self.index,
            "task": self.task,
            "done": self.done
        }