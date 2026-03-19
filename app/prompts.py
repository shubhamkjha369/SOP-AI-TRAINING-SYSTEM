def master_prompt(text, seed):
    return f"""
You are a senior corporate trainer. Generate structured training based on the SOP provided below.

Respond EXACTLY with the following 3 sections separated by the `===` delimiters:

=== SUMMARY ===
[Write a clear 1-to-2 paragraph summary covering objectives and scope]

=== STEPS ===
[List the core steps one by one, one per line]

=== TRAINING GUIDE ===
### 🎯 Learning Objectives
[Detail the exact goals the trainee should achieve]

### 📚 Context & Prerequisites
[Explain the background, why this process exists, and what the trainee needs before starting]

### 👥 Key Roles & Responsibilities
[Break down exactly who is involved and what they do]

### 🛠️ Required Systems & Tools
[List any physical or software tools required for this SOP]

### 📖 Deep-Dive Walkthrough
[Provide a highly detailed, extensive explanation of the process flow, expanding heavily on the core steps with context]

### 💡 Pro-Tips & Best Practices
[Provide insider advice to master this SOP]

### 🚫 Common Pitfalls
[List mistakes trainees usually make and how to avoid them]

### ⚠️ FAQs
[Anticipate and answer 3-5 common questions]

Rules:
- DO NOT stray from the requested format
- Make the TRAINING GUIDE section EXTREMELY DETAILED, COMPREHENSIVE, and EXTENSIVE. Act as a master instructor deeply explaining the entire SOP.
- Random seed: {seed}

SOP:
{text}
"""


def quiz_prompt(text, seed):
    return f"""
Generate a UNIQUE quiz from this SOP.

STRICT JSON:

{{
 "quiz": [
   {{
     "question": "...",
     "options": ["Option1", "Option2", "Option3", "Option4"],
     "answer": "A"
   }}
 ]
}}

Rules:
- Always create DIFFERENT questions
- Base ONLY on SOP
- 3–5 questions
- Shuffle logic

Random seed: {seed}

SOP:
{text}
"""