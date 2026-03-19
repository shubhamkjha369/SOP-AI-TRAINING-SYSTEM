import os
try:
    import streamlit as st
except ImportError:
    st = None

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from formatter import safe_json_loads

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
try:
    if not HF_API_TOKEN and st and hasattr(st, "secrets") and "HF_API_TOKEN" in st.secrets:
        HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
except Exception:
    pass

# ✅ Use the official InferenceClient which correctly routes API requests
client = InferenceClient(api_key=HF_API_TOKEN) if HF_API_TOKEN else None

MODEL = "Qwen/Qwen2.5-7B-Instruct"

def generate_quiz(sop_text):
    if not client:
        print("Quiz Generation error: HF_API_TOKEN is missing or invalid.")
        return [
            {
                "question": "API ERROR: HF_API_TOKEN missing. Please configure your Hugging Face API token in Streamlit secrets.",
                "options": ["A", "B", "C", "D"],
                "answer": "A"
            }
        ]

    prompt = f"""
You are a corporate trainer.

Generate a NEW quiz every time.

Return STRICT JSON ONLY, no markdown formatting or extra text:

{{
  "quiz": [
    {{
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "A"
    }}
  ]
}}

Rules:
- Create 3–5 questions
- Questions must be based ONLY on SOP
- Each run MUST generate DIFFERENT questions
- Avoid repeating patterns
- No explanation outside JSON

SOP:
{sop_text}
"""

    try:
        response = client.chat_completion(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=500
        )
        raw_output = response.choices[0].message.content
        print("Quiz Response preview:", raw_output[:100])
        return safe_json_loads(raw_output).get("quiz", [])
    except Exception as e:
        print("Quiz Generation error:", e)
        return []