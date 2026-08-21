# 🤝 SignBridge

### Bidirectional Sign Communication with Emergency Assistance

SignBridge is a software-based communication system designed to reduce communication barriers between sign-language users and people who communicate through speech.

The system provides:

- 🖐️ Sign → Text / Speech
- 🎤 Speech → Text
- 🚨 Emergency assistance
- 💬 Shared communication history

> SignBridge is an MVP with a predefined sign vocabulary. It does not claim to provide universal sign-language translation.

---

## 🚀 Features

### 🖐️ Sign → Text / Speech

The camera captures hand gestures and detects supported signs using hand landmarks and a machine-learning classifier.

Recognized gestures can be displayed as text and converted into speech.

### 🎤 Speech → Text

Spoken communication is captured through the microphone and converted into text for the sign-language user.

### 🚨 Emergency Assistance

Priority gestures can trigger emergency messages and visual alerts.

The system is designed to support critical communication such as HELP and other predefined emergency phrases.

### 💬 Communication History

Recognized sign messages and speech-to-text messages are displayed in a shared communication history.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────┐
                 │      Camera      │
                 └────────┬─────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Hand Landmark      │
                │ Extraction         │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Gesture Classifier │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Gesture Engine     │
                └──────┬─────┬───────┘
                       │     │
                       ▼     ▼
                    Text    Speech
                       │
                       ▼
                Communication
                   History


                 ┌──────────────────┐
                 │    Microphone    │
                 └────────┬─────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Speech Recognition │
                └─────────┬──────────┘
                          │
                          ▼
                       Text
                          │
                          ▼
                Communication History