import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# =========================
# 📊 LOAD DATA (SAFE)
# =========================

try:
    df = pd.read_csv("data/triage.csv")
    if df is None or df.empty:
        raise ValueError("Empty dataset")
except:
    df = pd.DataFrame()

# =========================
# 🔥 LABEL CONVERSION
# =========================

def convert_label(x):
    try:
        return 1 if float(x) >= 2 else 0
    except:
        return 0

# =========================
# 🤖 TRAIN MODEL (SAFE)
# =========================

if not df.empty and "triage_level" in df.columns:
    try:
        df["urgency"] = df["triage_level"].apply(convert_label)

        X = df.drop(["triage_level", "urgency"], axis=1)
        y = df["urgency"]

        X = pd.get_dummies(X)

        feature_columns = list(X.columns)

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            class_weight="balanced",
            random_state=42
        )

        model.fit(X, y)

    except:
        model = None
        feature_columns = []
else:
    model = None
    feature_columns = []

# =========================
# 🔍 SAFE ML FUNCTION
# =========================

def ml_ai(input_data: dict):
    try:
        # 🚨 fallback if model not ready
        if model is None or len(feature_columns) == 0:
            return 0, 0.5

        input_df = pd.DataFrame([input_data])

        input_df = pd.get_dummies(input_df)

        # ✅ ensure all training columns exist
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # ✅ keep only required columns
        input_df = input_df[feature_columns]

        # 🚨 safety check
        if input_df.shape[1] == 0:
            return 0, 0.5

        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0].max()

        return int(pred), float(prob)

    except:
        return 0, 0.5


# =========================
# 🔥 FINAL PREDICT (CRASH PROOF)
# =========================

def predict(input_data: dict):
    try:
        # 🛡️ SAFE INPUT HANDLING
        age = float(input_data.get("age", 0) or 0)
        hr = float(input_data.get("heart_rate", 0) or 0)
        bp = float(input_data.get("systolic_blood_pressure", 0) or 0)
        spo2 = float(input_data.get("oxygen_saturation", 100) or 100)
        temp = float(input_data.get("body_temperature", 37) or 37)
        pain = float(input_data.get("pain_level", 0) or 0)
        chronic = float(input_data.get("chronic_disease_count", 0) or 0)
        visits = float(input_data.get("previous_er_visits", 0) or 0)
        arrival = input_data.get("arrival_mode", "walk-in") or "walk-in"

        # =========================
        # 🚨 RULE-BASED LOGIC
        # =========================

        if spo2 < 85:
            return {
                "label": "urgent",
                "confidence": 0.98,
                "message": "🚨 Critical oxygen level",
                "color": "red"
            }

        if hr > 130 or temp > 39:
            return {
                "label": "urgent",
                "confidence": 0.95,
                "message": "🚨 High vital risk",
                "color": "red"
            }

        if pain > 8:
            return {
                "label": "urgent",
                "confidence": 0.9,
                "message": "⚠️ Severe pain detected",
                "color": "red"
            }

        # =========================
        # 🤖 ML PREDICTION
        # =========================

        safe_input = {
            "age": age,
            "heart_rate": hr,
            "systolic_blood_pressure": bp,
            "oxygen_saturation": spo2,
            "body_temperature": temp,
            "pain_level": pain,
            "chronic_disease_count": chronic,
            "previous_er_visits": visits,
            "arrival_mode": arrival
        }

        label, confidence = ml_ai(safe_input)

        if label == 1:
            return {
                "label": "urgent",
                "confidence": round(confidence, 2),
                "message": "🚨 Urgent - Seek immediate medical help!",
                "color": "red"
            }
        else:
            return {
                "label": "not_urgent",
                "confidence": round(confidence, 2),
                "message": "✅ Not Urgent - Monitor symptoms",
                "color": "green"
            }

    except Exception as e:
        # 🚨 ABSOLUTE FALLBACK (NEVER CRASH)
        return {
            "label": "not_urgent",
            "confidence": 0.5,
            "message": "Fallback prediction due to error",
            "error": str(e)
        }


# =========================
# 🧪 TEST
# =========================

if __name__ == "__main__":
    sample = {
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

    print(predict(sample))