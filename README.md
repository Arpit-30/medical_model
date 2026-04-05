---
title: Email Spam Env
emoji: 🚀
colorFrom: blue
colorTo: yellow
sdk: docker
pinned: false
license: mit
short_description: AI email spam detection using OpenEnv
---
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



