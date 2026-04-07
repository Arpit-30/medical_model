import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# =========================
# 📊 LOAD DATA
# =========================

df = pd.read_csv("data/triage.csv")

# 🔥 Convert to binary (IMPORTANT)
# 0 = not urgent, 1 = urgent
def convert_label(x):
    return 1 if x >= 2 else 0   # 2,3 = urgent

df["urgency"] = df["triage_level"].apply(convert_label)

# Features and target
X = df.drop(["triage_level", "urgency"], axis=1)
y = df["urgency"]

# One-hot encoding
X = pd.get_dummies(X)

# Save column structure
feature_columns = X.columns

# =========================
# 🤖 TRAIN MODEL (STRONG MODEL)
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight="balanced",
    random_state=42
)

model.fit(X, y)

# =========================
# 🔍 ML PREDICT FUNCTION
# =========================

def ml_ai(input_data: dict):
    input_df = pd.DataFrame([input_data])

    # One-hot encoding
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0].max()

    return pred, prob


# =========================
# 🔍 FINAL PREDICT
# =========================

def predict(input_data: dict):
    label, confidence = ml_ai(input_data)

    # 🔥 DEBUG (optional)
    print("Predicted urgency:", label)

    if label == 1:
        return {
            "label": "urgent",
            "confidence": round(float(confidence), 2),
            "message": "🚨 Urgent - Seek immediate medical help!",
            "color": "red"
        }
    else:
        return {
            "label": "not_urgent",
            "confidence": round(float(confidence), 2),
            "message": "✅ Not Urgent - Monitor symptoms",
            "color": "green"
        }


# =========================
# 🧪 TEST
# =========================

if __name__ == "__main__":
    sample_urgent = {
        "age": 60,
        "heart_rate": 150,
        "systolic_blood_pressure": 180,
        "oxygen_saturation": 85,
        "body_temperature": 40,
        "pain_level": 9,
        "chronic_disease_count": 2,
        "previous_er_visits": 3,
        "arrival_mode": "ambulance"
    }

    sample_normal = {
        "age": 25,
        "heart_rate": 75,
        "systolic_blood_pressure": 120,
        "oxygen_saturation": 98,
        "body_temperature": 36.8,
        "pain_level": 1,
        "chronic_disease_count": 0,
        "previous_er_visits": 0,
        "arrival_mode": "walk-in"
    }

    print("\n🚨 URGENT TEST:")
    print(predict(sample_urgent))

    print("\n✅ NORMAL TEST:")
    print(predict(sample_normal))