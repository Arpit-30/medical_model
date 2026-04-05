# 📧 AI Email Spam Detection (OpenEnv)

## 🚀 Overview

This project implements a **real-world email spam detection environment** using the OpenEnv specification.

The environment simulates how humans and AI systems classify emails into:

* **spam**
* **not_spam**

It provides:

* Sequential decision-making
* Reward-based learning
* Multi-level difficulty tasks

---

## 🧠 Motivation

Spam detection is widely used in:

* 📩 Email platforms (Gmail, Outlook)
* 🔐 Cybersecurity systems
* 💳 Fraud detection

This environment models real-world trade-offs:

* Avoid false positives (blocking real emails)
* Detect harmful spam effectively

---

## 📁 Project Structure

```text
email_env/
│
├── data/
│   └── emails_clean.csv
│
├── server/
│   ├── app.py
│   ├── email_env_environment.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── models.py
├── grader.py
├── inference.py
├── ui_app.py
├── openenv.yaml
└── README.md
```

---

## 🧩 Environment Design

### 👀 Observation Space

Each step returns:

* `email_text` → email content
* `has_link` → detects URLs (http/www)
* `has_money` → detects scam signals ($, £, prize, cash)
* `step_count` → step index

---

### 🎯 Action Space

Agent must choose:

* `spam`
* `not_spam`

---

### 🏆 Reward Function

| Condition                        | Reward |
| -------------------------------- | ------ |
| Correct classification           | +1.0   |
| False positive (not_spam → spam) | -1.0   |
| Missed spam                      | -0.5   |

👉 This reflects real-world systems where false positives are costly.

---

## 🎯 Tasks (Difficulty Levels)

### 🟢 Easy

* Small dataset
* Direct classification

### 🟡 Medium

* Uses signals:

  * links
  * spam keywords

### 🔴 Hard

* Multi-signal reasoning:

  * links
  * keywords
  * money detection

---

## 🤖 Baseline Agent

Implemented in `inference.py`

Two modes:

### 1. Rule-Based AI (Default)

* Uses keyword + link detection
* Fast and deterministic
* No API required

### 2. LLM-based AI (Optional)

* Uses OpenAI API (if key available)
* Falls back to rule-based if API fails

---

## 🔁 OpenEnv API

The environment follows OpenEnv standard:

* `reset()` → initialize environment
* `step(action)` → returns:

  * observation
  * reward
  * done
  * info
* `state()` → current state

---

## 🧪 Grading System

Implemented in `grader.py`

* Provides score between **0.0 – 1.0**
* Deterministic evaluation
* Tracks performance across tasks

---

## 🏗️ Architecture

User → UI → Environment → Agent → Action → Reward → Next State

---

## 🤔 Why Not Just Classification?

Unlike traditional ML classification:

* This is **sequential**
* Uses **reward feedback**
* Supports **reinforcement learning**
* Models **decision trade-offs**

---

## ▶️ Running the Project

### Run Agent (Inference)

```bash
python inference.py
```

---

### Run UI

```bash
python ui_app.py
```

---

## 📊 Output Format

```text
[START]
[STEP] task=easy action=spam reward=1.0 score=1.0
[RESULT] task=easy score=0.90
[END]
```

---

## 🐳 Docker

```bash
docker build -t email_env .
docker run -p 8000:8000 email_env
```

---

## ☁️ Deployment

This environment is designed for:

* Hugging Face Spaces (Docker)
* OpenEnv validation systems

---

## 📌 Key Features

* ✅ Real-world task simulation
* ✅ Multi-task environment (easy → hard)
* ✅ Reward shaping with partial signals
* ✅ Deterministic grading system
* ✅ UI for interaction
* ✅ Works without API (offline mode)
* ✅ OpenEnv compliant

---

## 🏁 Results

* ~85–95% accuracy
* Stable across tasks
* Reproducible baseline scores

---

## 🏆 Conclusion

This project demonstrates how spam detection can be modeled as:

* A reinforcement learning environment
* A sequential decision system
* A real-world AI simulation

It is useful for:

* Training agents
* Evaluating AI models
* Research experiments
