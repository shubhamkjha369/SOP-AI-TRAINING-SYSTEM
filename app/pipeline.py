from extractor import extract_text
from processor import clean_text, structure_text
from ai_engine import call_llm
from prompts import master_prompt
from formatter import safe_json_loads
from quiz_engine import generate_quiz
import re


# ✅ STRONG STEP EXTRACTION
def extract_steps_from_text(text):
    steps = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if re.match(r'^\d+\.', line):  # matches 1. 2. 3. ... ANY number
            steps.append(line)

        elif line.lower().startswith("step"):
            steps.append(line)

    return steps


def run_pipeline(file):
    raw_text = extract_text(file)
    cleaned = clean_text(raw_text)

    if not cleaned:
        cleaned = "Sample SOP: Reset password by clicking forgot password and following instructions."

    # ✅ HF Context Limit Protection (Max ~32k tokens)
    # 1 token ~= 4 chars. 25,000 tokens ~= 100,000 chars.
    MAX_CHARS = 100000
    if len(cleaned) > MAX_CHARS:
        import streamlit as st
        st.warning(f"⚠️ **Warning**: The uploaded SOP is excessively large ({len(cleaned):,} characters). Truncating to the first {MAX_CHARS:,} characters (~25 pages) to fit within the AI's memory limit.")
        cleaned = cleaned[:MAX_CHARS]

    structured = structure_text(cleaned)

    # ✅ FORCE RANDOMNESS FOR QUIZ VARIATION
    import random
    random_hint = str(random.randint(0, 100000))

    response = call_llm(master_prompt(structured, random_hint))

    # Return RAW RESPONSE if it's an API Error
    if response.startswith("API ERROR:"):
        return {
            "summary": response,
            "steps": [response],
            "training_guide": response,
            "quiz": generate_quiz(structured)
        }

    import re
    result = {"summary": "", "steps": [], "training_guide": ""}
    
    # Extract Summary
    sum_match = re.search(r'=+\s*SUMMARY\s*=+\s*([\s\S]*?)=+\s*STEPS\s*=+', response, re.IGNORECASE)
    if sum_match: result["summary"] = sum_match.group(1).strip()
    
    # Extract Steps
    step_match = re.search(r'=+\s*STEPS\s*=+\s*([\s\S]*?)=+\s*TRAINING GUIDE\s*=+', response, re.IGNORECASE)
    if step_match:
        steps_text = step_match.group(1).strip()
        result["steps"] = [s.strip() for s in steps_text.split('\n') if s.strip()]
        
    # Extract Training Guide
    train_match = re.search(r'=+\s*TRAINING GUIDE\s*=+\s*([\s\S]*)', response, re.IGNORECASE)
    if train_match: 
        result["training_guide"] = train_match.group(1).strip()

    summary = result.get("summary", "")
    steps = result.get("steps", [])
    training = result.get("training_guide", "")
    
    # ✅ CALL QUIZ ENGINE
    quiz = generate_quiz(structured)

    # ✅ SUMMARY FIX
    if not summary:
        summary = f"DEBUG TRACE (Failed to find SUMMARY Block):\n\n{response}"

    # ✅ STEP FIX
    if not steps or len(steps) < 2:
        extracted = extract_steps_from_text(cleaned)
        steps = extracted if extracted else [f"DEBUG TRACE:\n{response}"]

    # ✅ TRAINING FIX
    if not training:
        training = f"DEBUG TRACE (Failed to find TRAINING Block):\n\n{response}"

    # ✅ QUIZ FIX
    if not quiz:
        quiz = [
            {
                "question": "Error generating quiz. Please check API configuration or SOP content.",
                "options": ["A", "B", "C", "D"],
                "answer": "A"
            }
        ]

    return {
        "summary": summary,
        "steps": steps,
        "training_guide": training,
        "quiz": quiz
    }