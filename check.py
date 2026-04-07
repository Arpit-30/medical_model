import pandas as pd

df = pd.read_csv("data/triage.csv")   # 🔥 THIS LINE WAS MISSING

print(df["triage_level"].value_counts())