import pandas as pd

# 📊 Load your raw medical dataset
# 👉 Change file name if needed
df = pd.read_csv("data/medical_raw.csv")

# 🧹 Standardize column names
df = df.rename(columns={
    "symptoms": "text",
    "urgency": "label"
})

# Keep only required columns
df = df[["text", "label"]]

# 🏷️ Normalize labels
df["label"] = df["label"].str.lower()

df["label"] = df["label"].map({
    "urgent": "urgent",
    "not urgent": "not_urgent",
    "not_urgent": "not_urgent",
    "low": "not_urgent",
    "high": "urgent"
})

# ❌ Remove missing values
df = df.dropna()

# 🔄 Remove duplicates
df = df.drop_duplicates()

# 💾 Save cleaned dataset
df.to_csv("data/triage.csv", index=False)

print("✅ Medical dataset cleaned and saved as triage.csv")