import gradio as gr
from inference import predict

# 🎨 CSS
css = """
body {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec);
    font-family: 'Segoe UI', sans-serif;
}

#title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #0d47a1;
}

#subtitle {
    text-align: center;
    color: #444;
    margin-bottom: 20px;
    font-size: 16px;
}

button {
    background: linear-gradient(90deg, #42a5f5, #7e57c2) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px;
    font-size: 16px;
}

button:hover {
    background: linear-gradient(90deg, #1e88e5, #5e35b1) !important;
}

.result-box {
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    padding: 20px;
}
"""

# 🔍 Prediction wrapper
def ui_predict(age, heart_rate, bp, oxygen, temp, pain, disease, visits, mode):
    input_data = {
        "age": age,
        "heart_rate": heart_rate,
        "systolic_blood_pressure": bp,
        "oxygen_saturation": oxygen,
        "body_temperature": temp,
        "pain_level": pain,
        "chronic_disease_count": disease,
        "previous_er_visits": visits,
        "arrival_mode": mode
    }

    result = predict(input_data)

    return f"""
    <div style="color:{result['color']};">
        {result['message']}<br><br>
        Confidence: {result['confidence']}
    </div>
    """

# 🎨 UI
with gr.Blocks(css=css) as demo:

    gr.Markdown("<div id='title'>🏥 Medical Triage AI</div>")
    gr.Markdown("<div id='subtitle'>AI-powered urgency detection</div>")

    with gr.Row():
        age = gr.Slider(0, 100, value=30, label="Age")
        heart_rate = gr.Slider(40, 180, value=80, label="Heart Rate")

    with gr.Row():
        bp = gr.Slider(80, 200, value=120, label="Blood Pressure")
        oxygen = gr.Slider(70, 100, value=98, label="Oxygen Saturation")

    with gr.Row():
        temp = gr.Slider(35, 42, value=37, label="Body Temperature")
        pain = gr.Slider(0, 10, value=2, label="Pain Level")

    with gr.Row():
        disease = gr.Number(value=0, label="Chronic Disease Count")
        visits = gr.Number(value=0, label="Previous ER Visits")

    mode = gr.Dropdown(
        ["walk-in", "ambulance"],
        value="walk-in",
        label="Arrival Mode"
    )

    btn = gr.Button("🔍 Check Urgency")
    output = gr.HTML(elem_classes="result-box")

    btn.click(
        ui_predict,
        inputs=[age, heart_rate, bp, oxygen, temp, pain, disease, visits, mode],
        outputs=output
    )

# 🚀 Launch
demo.launch()