import os
import random
try:
    import streamlit as st
except ImportError:
    st = None

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
try:
    if not HF_API_TOKEN and st and hasattr(st, "secrets") and "HF_API_TOKEN" in st.secrets:
        HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
except Exception:
    pass

# ✅ Use the official InferenceClient which correctly routes API requests
client = InferenceClient(api_key=HF_API_TOKEN) if HF_API_TOKEN else None

# ✅ Using an accessible, open-source state-of-the-art model that cleanly produces JSON
MODEL = "Qwen/Qwen2.5-7B-Instruct"

def call_llm(prompt, retries=3):
    if not client:
        print("Error: HF_API_TOKEN missing in .env and secrets")
        return "API ERROR: HF_API_TOKEN missing. Please configure your Hugging Face API token in .env or Streamlit secrets."

    # 🔥 Add randomness to force different outputs (CRITICAL for quiz regen)
    random_hint = str(random.randint(0, 100000))
    prompt = prompt.strip() + f"\n\nRandom Seed: {random_hint}"

    for _ in range(retries):
        try:
            response = client.chat_completion(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            output = response.choices[0].message.content
            print("LLM Response preview:", output[:100])
            return output
            
        except Exception as e:
            err_msg = str(e)
            print("HF API Error:", err_msg)
            import time
            time.sleep(3)

    return f"API ERROR: {err_msg}"