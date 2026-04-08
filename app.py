import gradio as gr
from inference import predict
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 🎨 CSS — Dark Medical Tech Theme
css = """
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:    #0a0f1e;
    --bg-card:       #111827;
    --bg-glass:      rgba(255,255,255,0.04);
    --border:        rgba(99,179,237,0.18);
    --accent-blue:   #63b3ed;
    --accent-cyan:   #76e4f7;
    --accent-violet: #b794f4;
    --accent-green:  #68d391;
    --accent-red:    #fc8181;
    --text-primary:  #f0f4ff;
    --text-muted:    #8896b3;
    --font-ui:       'DM Sans', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius:        14px;
    --glow-blue:     0 0 24px rgba(99,179,237,0.25);
    --glow-violet:   0 0 24px rgba(183,148,244,0.25);
    --slider-color:  #63b3ed !important;
    --color-accent:  #63b3ed !important;
}

/* ── Base Reset ── */
*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    background: var(--bg-primary) !important;
    font-family: var(--font-ui) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* ── Animated Background Mesh ── */
.gradio-container::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 20% 10%, rgba(99,179,237,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 50% at 80% 80%, rgba(183,148,244,0.07) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(118,228,247,0.04) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Panels & Cards — overflow MUST be visible for dropdown ── */
.gr-block, .gr-box, .gr-panel,
.gradio-container .block,
.gradio-container .panel,
.gradio-container .wrap,
.gradio-container .contain,
.gradio-container .form,
.gradio-container {
    overflow: visible !important;
}

/* Keep card styling but allow overflow */
.gr-block, .gr-box, .gr-panel,
.gradio-container .block,
.gradio-container .panel {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
    backdrop-filter: blur(12px);
}

/* ── Labels ── */
label, .gr-label, span.svelte-1gfkn6j {
    font-family: var(--font-ui) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ── Sliders ── */
input[type="range"] {
    -webkit-appearance: none !important;
    appearance: none !important;
    accent-color: var(--accent-blue) !important;
    height: 6px !important;
    border-radius: 99px !important;
    background: rgba(99,179,237,0.15) !important;
    outline: none !important;
    width: 100% !important;
    cursor: pointer;
}

input[type="range"]::-webkit-slider-runnable-track {
    -webkit-appearance: none !important;
    height: 6px !important;
    border-radius: 99px !important;
    background: rgba(99,179,237,0.15) !important;
}

input[type="range"]::-moz-range-track {
    height: 6px !important;
    border-radius: 99px !important;
    background: rgba(99,179,237,0.15) !important;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none !important;
    appearance: none !important;
    background: var(--accent-cyan) !important;
    box-shadow: 0 0 10px rgba(118,228,247,0.7), 0 0 4px rgba(118,228,247,0.4) !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    margin-top: -6px !important;
    border: 2px solid var(--bg-card) !important;
    cursor: pointer;
    transition: box-shadow 0.2s, transform 0.15s;
}

input[type="range"]::-moz-range-thumb {
    background: var(--accent-cyan) !important;
    box-shadow: 0 0 10px rgba(118,228,247,0.7) !important;
    border-radius: 50% !important;
    width: 18px !important;
    height: 18px !important;
    border: 2px solid var(--bg-card) !important;
    cursor: pointer;
}

input[type="range"]:hover::-webkit-slider-thumb {
    transform: scale(1.2);
    box-shadow: 0 0 16px rgba(118,228,247,0.9), 0 0 6px rgba(118,228,247,0.5) !important;
}

/* Gradio svelte slider track fill */
.gradio-container .track,
.gradio-container .track-fill {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
    height: 6px !important;
    border-radius: 99px !important;
}

.gradio-container .track {
    background: rgba(99,179,237,0.15) !important;
}

/* ── Number Inputs ── */
input[type="number"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}

input[type="number"]:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--glow-blue) !important;
    outline: none !important;
}

/* ══════════════════════════════════════════
   ── Dropdown — targeting real Gradio DOM ──
   ══════════════════════════════════════════ */

/* The outer dropdown container */
.gradio-container .wrap-inner,
.gradio-container .multiselect {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    min-height: 44px !important;
    padding: 8px 12px !important;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.gradio-container .wrap-inner:hover,
.gradio-container .multiselect:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--glow-blue) !important;
}

/* Selected value text inside dropdown */
.gradio-container .wrap-inner span,
.gradio-container .wrap-inner .token,
.gradio-container .secondary-wrap span {
    color: var(--text-primary) !important;
    font-family: var(--font-ui) !important;
    font-size: 14px !important;
}

/* The floating options list */
.gradio-container ul.options {
    background: #1a2235 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 6px !important;
    margin-top: 4px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(99,179,237,0.1) !important;
    z-index: 99999 !important;
    position: absolute !important;
    overflow: hidden !important;
    backdrop-filter: blur(16px) !important;
}

/* Each option item */
.gradio-container ul.options li,
.gradio-container ul.options .item {
    color: var(--text-primary) !important;
    font-family: var(--font-ui) !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    border-radius: 6px !important;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    list-style: none !important;
}

.gradio-container ul.options li:hover,
.gradio-container ul.options .item:hover {
    background: rgba(99,179,237,0.15) !important;
    color: var(--accent-cyan) !important;
}

/* Active/selected item */
.gradio-container ul.options li.selected,
.gradio-container ul.options li[aria-selected="true"] {
    background: rgba(99,179,237,0.2) !important;
    color: var(--accent-blue) !important;
}

/* Chevron arrow icon inside dropdown */
.gradio-container .wrap-inner svg,
.gradio-container .dropdown-arrow {
    color: var(--text-muted) !important;
    fill: var(--text-muted) !important;
}

/* ── Primary Button ── */
button.primary, .gr-button-primary, button[variant="primary"],
.gradio-container button {
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-violet) 100%) !important;
    color: #0a0f1e !important;
    font-family: var(--font-ui) !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 14px 28px !important;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 20px rgba(99,179,237,0.35), var(--glow-violet) !important;
}

button.primary::after, .gradio-container button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.2s;
    border-radius: inherit;
}

button.primary:hover, .gradio-container button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 32px rgba(99,179,237,0.5), var(--glow-violet) !important;
}

button.primary:hover::after, .gradio-container button:hover::after {
    opacity: 1;
}

button.primary:active, .gradio-container button:active {
    transform: translateY(0) scale(0.99) !important;
}

/* ── Result / Output Box ── */
.result-box, .gr-html {
    background: linear-gradient(135deg, rgba(99,179,237,0.06), rgba(183,148,244,0.06)) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 28px 24px !important;
    text-align: center;
    font-family: var(--font-ui) !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    min-height: 80px;
    backdrop-filter: blur(8px);
    transition: box-shadow 0.3s;
}

.result-box:not(:empty) {
    animation: result-glow 0.5s ease forwards;
}

@keyframes result-glow {
    0%   { box-shadow: none; }
    50%  { box-shadow: 0 0 32px rgba(99,179,237,0.3); }
    100% { box-shadow: 0 0 16px rgba(99,179,237,0.15); }
}

/* ── Markdown / Subtitle ── */
.gr-markdown p, .prose p {
    color: var(--text-muted) !important;
    font-size: 14px !important;
    font-family: var(--font-ui) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

/* ── Row spacing ── */
.gr-row { gap: 16px !important; }

/* ── Fade-in on load ── */
.gradio-container > * {
    animation: fadein 0.6s ease both;
}

@keyframes fadein {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
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
    <div style="color:{result['color']}; font-size:20px; font-family:'DM Sans',sans-serif; font-weight:700; letter-spacing:0.01em;">
        {result['message']}<br><br>
        <span style="font-size:14px; font-weight:400; opacity:0.75; font-family:'JetBrains Mono',monospace;">
            Confidence: {result['confidence']}
        </span>
    </div>
    """

# 🎨 UI
with gr.Blocks() as demo:
    demo.css = css

    gr.HTML("""
    <div style="text-align: center; padding: 36px 0 8px;">
        <div style="display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #63b3ed; background: rgba(99,179,237,0.1); border: 1px solid rgba(99,179,237,0.25); border-radius: 99px; padding: 4px 16px; margin-bottom: 16px;">AI-Powered Emergency Triage</div>
        <div style="font-size: 44px; font-weight: 800; font-family: 'DM Sans', sans-serif; background: linear-gradient(90deg, #63b3ed, #76e4f7, #b794f4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.15; margin-bottom: 12px;">🏥 Medical Triage AI</div>
        <div style="width: 60px; height: 3px; background: linear-gradient(90deg, #63b3ed, #b794f4); border-radius: 99px; margin: 20px auto 0;"></div>
    </div>
    """)

    with gr.Row():
        age        = gr.Slider(0, 100,   value=30,  label="Age")
        heart_rate = gr.Slider(40, 180,  value=80,  label="Heart Rate (bpm)")

    with gr.Row():
        bp      = gr.Slider(80, 200,  value=120, label="Systolic Blood Pressure")
        oxygen  = gr.Slider(70, 100,  value=98,  label="Oxygen Saturation (%)")

    with gr.Row():
        temp = gr.Slider(35, 42, value=37, label="Body Temperature (°C)")
        pain = gr.Slider(0, 10,  value=2,  label="Pain Level (0–10)")

    with gr.Row():
        disease = gr.Number(value=0, label="Chronic Disease Count")
        visits  = gr.Number(value=0, label="Previous ER Visits")

    mode = gr.Dropdown(
        ["walk-in", "ambulance"],
        value="walk-in",
        label="Arrival Mode"
    )

    btn    = gr.Button("🔍 Assess Urgency", variant="primary")
    output = gr.HTML(elem_classes="result-box")

    btn.click(
        ui_predict,
        inputs=[age, heart_rate, bp, oxygen, temp, pain, disease, visits, mode],
        outputs=output
    )

    gr.HTML("""
    <div style="text-align:center;padding:24px 0 8px;font-size:12px;color:#4a5568;font-family:'DM Sans',sans-serif;letter-spacing:0.03em;">
        For clinical decision support only &middot; Not a substitute for professional medical judgment
    </div>
    <script>
    (function() {
        function fixSliders() {
            document.querySelectorAll('input[type="range"]').forEach(function(input) {
                var min = parseFloat(input.min) || 0;
                var max = parseFloat(input.max) || 100;
                var val = parseFloat(input.value) || 0;
                var pct = ((val - min) / (max - min)) * 100;
                input.style.setProperty('accent-color', '#63b3ed', 'important');
                input.style.setProperty('background',
                    'linear-gradient(90deg, #63b3ed ' + pct + '%, rgba(99,179,237,0.15) ' + pct + '%)',
                    'important');
            });
        }
        function fixDropdownOverflow() {
            document.querySelectorAll('ul.options').forEach(function(ul) {
                var el = ul.parentElement;
                var depth = 0;
                while (el && depth < 14) {
                    el.style.setProperty('overflow', 'visible', 'important');
                    el = el.parentElement;
                    depth++;
                }
                var trigger = ul.closest('.block, .wrap, [data-testid="dropdown"]');
                if (!trigger) trigger = ul.parentElement;
                var rect = trigger.getBoundingClientRect();
                ul.style.setProperty('position', 'fixed', 'important');
                ul.style.setProperty('top', (rect.bottom + 4) + 'px', 'important');
                ul.style.setProperty('left', rect.left + 'px', 'important');
                ul.style.setProperty('width', rect.width + 'px', 'important');
                ul.style.setProperty('z-index', '999999', 'important');
                ul.style.setProperty('overflow', 'hidden', 'important');
                ul.style.setProperty('bottom', 'unset', 'important');
                ul.style.setProperty('transform', 'none', 'important');
            });
        }
        fixSliders();
        fixDropdownOverflow();
        var observer = new MutationObserver(function() { fixSliders(); fixDropdownOverflow(); });
        observer.observe(document.body, {childList:true, subtree:true, attributes:true, attributeFilter:['style','class']});
        document.addEventListener('input', function(e) {
            if (e.target && e.target.type === 'range') {
                var min = parseFloat(e.target.min) || 0;
                var max = parseFloat(e.target.max) || 100;
                var val = parseFloat(e.target.value) || 0;
                var pct = ((val - min) / (max - min)) * 100;
                e.target.style.setProperty('background',
                    'linear-gradient(90deg, #63b3ed ' + pct + '%, rgba(99,179,237,0.15) ' + pct + '%)',
                    'important');
            }
        }, true);
    })();
    </script>
    """)

# 🚀 FastAPI + Gradio — /reset route MUST be added BEFORE mounting
app = FastAPI()

@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/predict")
def predict_api(data: dict):
    return predict(data)

# Mount Gradio LAST — after all FastAPI routes are registered
app = gr.mount_gradio_app(app, demo, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)