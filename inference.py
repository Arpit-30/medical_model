# =========================
# 🔥 FINAL CRASH-PROOF VERSION (NO ML)
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

        # =========================
        # 🚨 STRONG RULE ENGINE
        # =========================

        score = 0

        # Critical conditions
        if spo2 < 85:
            return {
                "label": "urgent",
                "confidence": 0.99,
                "message": "🚨 Critical oxygen level",
                "color": "red"
            }

        if hr > 130:
            score += 2

        if temp > 39:
            score += 2

        if pain > 8:
            score += 2

        if bp > 180:
            score += 2

        if chronic >= 2:
            score += 1

        if visits >= 3:
            score += 1

        if age > 65:
            score += 1

        # =========================
        # 🎯 FINAL DECISION
        # =========================

        if score >= 4:
            return {
                "label": "urgent",
                "confidence": 0.9,
                "message": "🚨 High risk patient",
                "color": "red"
            }

        elif score >= 2:
            return {
                "label": "urgent",
                "confidence": 0.75,
                "message": "⚠️ Moderate risk",
                "color": "orange"
            }

        else:
            return {
                "label": "not_urgent",
                "confidence": 0.7,
                "message": "✅ Stable condition",
                "color": "green"
            }

    except Exception as e:
        # 🚨 NEVER CRASH
        return {
            "label": "not_urgent",
            "confidence": 0.5,
            "message": "Fallback prediction",
            "error": str(e)
        }