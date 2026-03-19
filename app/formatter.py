import json
import re


def safe_json_loads(text):
    if not text:
        return {}

    # 🔹 Step 1: Try direct parse
    try:
        return json.loads(text, strict=False)
    except:
        pass

    # 🔹 Step 2: Extract using rfind (robust against bad regex logic)
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    
    if first_brace != -1 and last_brace != -1:
        json_str = text[first_brace:last_brace+1].strip()
        try:
            return json.loads(json_str, strict=False)
        except:
            pass

    # 🔹 Step 3: Try fixing quotes
    try:
        fixed = text.replace("'", '"')
        return json.loads(fixed, strict=False)
    except:
        pass

    # 🔹 Final fallback
    return {}


def format_output(summary, steps, training, quiz):
    # 🔹 Ensure correct types

    if not isinstance(steps, list):
        steps = [str(steps)]

    if not isinstance(quiz, list):
        quiz = []

    # 🔹 Clean steps
    steps = [str(s).strip() for s in steps if str(s).strip()]

    # 🔹 Clean quiz
    cleaned_quiz = []
    for q in quiz:
        if isinstance(q, dict):
            question = q.get("question", "")
            options = q.get("options", [])
            answer = q.get("answer", "")

            if question and isinstance(options, list) and answer:
                cleaned_quiz.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })

    return {
        "summary": str(summary).strip(),
        "steps": steps,
        "training_guide": str(training).strip(),
        "quiz": cleaned_quiz
    }