import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = None
feature_columns = []


# =========================
# 🔥 SAFE MODEL INIT (LAZY LOAD)
# =========================

def load_model():
    global model, feature_columns

    if model is not None:
        return

    try:
        df = pd.read_csv("data/triage.csv")

        if df is None or df.empty:
            return

        def convert_label(x):
            try:
                return 1 if float(x) >= 2 else 0
            except:
                return 0

        df["urgency"] = df["triage_level"].apply(convert_label)

        X = df.drop(["triage_level", "urgency"], axis=1)
        y = df["urgency"]

        X = pd.get_dummies(X)
        feature_columns = list(X.columns)

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(X, y)

    except:
        model = None
        feature_columns = []


# =========================
# 🔍 SAFE ML
# =========================

def ml_ai(input_data):
    try:
        load_model()

        if model is None or len(feature_columns) == 0:
            return 0, 0.5

        input_df = pd.DataFrame([input_data])
        input_df = pd.get_dummies(input_df)

        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[feature_columns]

        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0].max()

        return int(pred), float(prob)

    except:
        return 0, 0.5


# =========================
# 🔥 FINAL PREDICT
# =========================

def predict(input_data: dict):
    try:
        age = float(input_data.get("age", 0) or 0)
        hr = float(input_data.get("heart_rate", 0) or 0)
        spo2 = float(input_data.get("oxygen_saturation", 100) or 100)
        temp = float(input_data.get("body_temperature", 37) or 37)
        pain = float(input_data.get("pain_level", 0) or 0)

        # 🚨 RULES
        if spo2 < 85:
            return {"label": "urgent", "confidence": 0.98}

        if hr > 130 or temp > 39:
            return {"label": "urgent", "confidence": 0.95}

        if pain > 8:
            return {"label": "urgent", "confidence": 0.9}

        label, confidence = ml_ai(input_data)

        return {
            "label": "urgent" if label == 1 else "not_urgent",
            "confidence": round(confidence, 2)
        }

    except:
        return {
            "label": "not_urgent",
            "confidence": 0.5
        }