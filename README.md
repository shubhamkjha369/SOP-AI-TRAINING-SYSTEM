# 📘 SOP → AI Training System

## 🚀 Overview
The **SOP → AI Training System** is an automated pipeline designed to solve a critical HR and operations bottleneck: *training employees using static Standard Operating Procedure (SOP) documents is manual, boring, and time-consuming.*

This application seamlessly ingestion raw SOP texts or PDFs and uses Advanced Large Language Models (LLMs) to automatically generate highly structured, interactive learning funnels consisting of:
1. **Executive Summaries**
2. **Step-by-Step Task Breakdowns**
3. **Comprehensive Training Guides** (Roles, Objectives, FAQs)
4. **Interactive Validation Quizzes**

---

## 🏗️ Architecture & Tech Stack

This project was built focusing on **practicality, reliability, and cost-effectiveness**.

* **Frontend:** [Streamlit](https://streamlit.io/) - Provides a lightweight, instant web-dashboard that feels incredibly interactive (featuring dynamic loading states, persistent tab locations, and form-based quiz submission).
* **AI Orchestration Framework:** Pure Python (no heavy frameworks like LangChain were used to adhere to the "Do not over-engineer" requirement).
* **LLM Provider:** Hugging Face `InferenceClient`.
* **Model:** `Qwen/Qwen2.5-7B-Instruct` - Chosen because it is an incredibly capable, open-source 7B parameter model that runs efficiently on free-tier inference APIs.

---

## 🧠 Key Technical Decisions

### 1. Bulletproof Markdown Parsing Over JSON
Most AI wrappers attempt to force LLMs to output massive blocks of text wrapped in strict JSON format. When doing this on large SOPs (e.g., 4KB+ texts), open-source 7B models frequently introduce syntax errors (like unescaped quotes or missing commas) which immediately crash Python's `json.loads` decoder, causing the app to fail.

To make this pipeline **100% resilient**, the main Training Engine uses a custom Markdown Block extraction system (e.g., `=== SUMMARY ===`). This guarantees that no matter how much text or weird formatting the AI generates, the system perfectly slices out your content without crashing.

### 2. Token Limit Management
Free-tier endpoints have hard context limits (usually 4096 tokens). The prompt engineering in this application was meticulously refined to strike the perfect balance between depth and conciseness—ensuring that the combined prompt + output never breaches token limits, meaning the AI will never abruptly cut off mid-generation.

---

## ⚙️ Setup & Installation

### Prerequisites
Make sure you have Python 3.9+ installed on your machine.

### 1. Clone the repository and install dependencies
```bash
# It is highly recommended to use a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Environment Variables
You need a Hugging Face API Token (it is completely free to generate one).
1. Go to [Hugging Face](https://huggingface.co/) and create an account.
2. Navigate to your Settings -> Access Tokens.
3. Create a `.env` file in the root directory of this project and add your token:
```env
HF_API_TOKEN=hf_your_token_here
```

### 3. Run the Application
Start the Streamlit dashboard:
```bash
streamlit run app/main.py
```
Upload an SOP `.txt` or `.pdf` file in the browser, and click **🚀 Generate Training**.

---

## 📈 Future Scaling & Automation

This MVP is designed to easily plug into enterprise architecture:
* **Webhook Integration:** Output JSONs can be caught via Zapier or Make.com to dynamically blast emails to new hires via Zendesk/Gmail whenever HR uploads an SOP.
* **Database Integration:** Quizzes can report back scores directly into an internal SQL database or Google Sheets to track employee compliance.

*(See `improvements_and_scaling.md` for dedicated infrastructure scaling thoughts).*
