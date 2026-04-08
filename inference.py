# =========================
# 🚀 ULTRA SAFE FINAL VERSION
# =========================

def predict(input_data):
    try:
        # 🛡️ Safe extraction
        age = float(input_data.get("age", 0) or 0)
        hr = float(input_data.get("heart_rate", 0) or 0)
        bp = float(input_data.get("systolic_blood_pressure", 0) or 0)
        spo2 = float(input_data.get("oxygen_saturation", 100) or 100)
        temp = float(input_data.get("body_temperature", 37) or 37)
        pain = float(input_data.get("pain_level", 0) or 0)

        # 🚨 critical condition
        if spo2 < 85:
            return {"label": "urgent", "confidence": 0.99}

        # 🎯 scoring
        score = 0

        if hr > 130:
            score += 2
        if temp > 39:
            score += 2
        if pain > 8:
            score += 2
        if bp > 180:
            score += 2
        if age > 65:
            score += 1

        # 🎯 decision
        if score >= 4:
            return {"label": "urgent", "confidence": 0.9}
        elif score >= 2:
            return {"label": "urgent", "confidence": 0.75}
        else:
            return {"label": "not_urgent", "confidence": 0.7}

    except:
        # 🚨 NEVER crash
        return {"label": "not_urgent", "confidence": 0.5}