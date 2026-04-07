---
title: Medical Triage AI
emoji: 🏥
colorFrom: red
colorTo: green
sdk: gradio
pinned: false
license: mit
short_description: AI app to detect urgent medical cases
---

# 🏥 Medical Triage AI (Urgent vs Not Urgent)

## 🚀 Overview

This project is an **AI-powered medical triage system** that classifies symptoms into:

- 🚨 **Urgent**
- ✅ **Not Urgent**

It uses **Machine Learning (Logistic Regression)** to help users quickly assess whether medical attention is needed.

---

## 🧠 Motivation

In real life, people often struggle to decide:

- "Is this serious?"
- "Should I go to the hospital?"

This system helps by:

- ⚡ Providing instant guidance  
- 🧠 Using AI for decision support  
- 🏥 Assisting early triage in healthcare  

---

## 🛠️ Tech Stack

- **Machine Learning:** Logistic Regression (scikit-learn)
- **Text Processing:** TF-IDF Vectorization
- **Frontend:** Gradio (UI)
- **Backend:** FastAPI (optional API)
- **Language:** Python

---

## 📁 Project Structure

```text
medical_ai/
│
├── data/
│   └── triage.csv
│
├── server/
│   └── app.py          # FastAPI backend
│
├── app.py              # Gradio UI
├── inference.py        # ML prediction logic
├── models.py           # Data models
├── grader.py           # Evaluation
├── fix_csv.py          # Dataset cleaner
├── requirements.txt
└── README.md