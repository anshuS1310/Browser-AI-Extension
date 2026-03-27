# 🌌 Browser AI Extension
> **Your Research & Analysis Companion**

A modern, local-first Chrome extension that bridges your browsing experience with high-performance Transformer models. Analyze research papers, summarize long articles, and get detailed AI-driven explanations—all from a sleek, dark-themed side panel.

---

## ✨ Features

* **⚡ Instant Snippet Analysis:** Highlight any text on a webpage, and it automatically "jumps" into the AI input box with a smooth visual bounce.
* **📖 Full-Page Summarization:** One click extracts the entire visible content of a tab and sends it to the AI for a comprehensive, long-form breakdown.
* **🧠 Local LLM Power:** Powered by `google/flan-t5-base` (or small), providing "Gemini-style" detailed responses without sending data to the cloud.
* **🎨 Aesthetic Dark UI:** A premium "Midnight Obsidian" interface with neon purple accents, frosted glass effects, and scrollable response cards.
* **🔒 Privacy-Centric:** Your data stays on your machine. The extension communicates only with your local Python backend.

---

## 🛠️ Technical Architecture

* **Frontend:** HTML5, CSS3 (Inter Font, Font Awesome), JavaScript (Chrome Extension MV3).
* **Backend:** Python 3.x, Flask, Flask-CORS.
* **AI Engine:** Hugging Face `transformers` library using **Flan-T5**.
* **Hardware:** Optimized for local CPU/GPU inference with repetition penalties to ensure high-quality, non-looping output.

---

## 🚀 Installation & Setup

### 1. The Python Engine (Backend)
Ensure you have Python installed, then set up the required environment:

```bash
# Install dependencies
pip install flask flask-cors transformers torch sentencepiece

# Run the server
python app.py
