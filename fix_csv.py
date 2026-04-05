import pandas as pd

df = pd.read_csv("data/spam mail.csv", encoding="latin-1")

# rename columns
df = df.rename(columns={
    "Category": "label",
    "Masseges": "text"
})

# FIX: swap columns order
df = df[["text", "label"]]

# convert labels
df["label"] = df["label"].map({
    "ham": "not_spam",
    "spam": "spam"
})

df.to_csv("data/emails_clean.csv", index=False)

print("✅ Fixed CSV properly")