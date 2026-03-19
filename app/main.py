import streamlit as st
from pipeline import run_pipeline
import json
import random
import re

st.set_page_config(page_title="SOP AI Trainer", layout="wide")

st.title("📘 SOP → AI Training Generator")
st.divider()

# -----------------------
# SESSION
# -----------------------
if "result" not in st.session_state:
    st.session_state.result = None

# -----------------------
# UPLOAD
# -----------------------
file = st.file_uploader("Upload SOP", type=["pdf", "txt"])

if file:
    st.success(file.name)

    if st.button("🚀 Generate Training"):
        with st.spinner("Processing SOP and Generating AI Training Content..."):
            st.session_state.result = run_pipeline(file)

    if st.session_state.result:
        if st.button("🔁 Regenerate Quiz"):
            with st.spinner("Regenerating Quiz..."):
                new = run_pipeline(file)
                st.session_state.result["quiz"] = new["quiz"]
                st.session_state.active_tab = "Quiz"
                st.rerun()

# -----------------------
# DISPLAY
# -----------------------
if st.session_state.result:
    result = st.session_state.result

    tabs = ["Summary", "Steps", "Training", "Quiz"]
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Summary"

    active_tab = st.radio("Navigation", tabs, horizontal=True, label_visibility="collapsed", key="active_tab")
    st.divider()

    # -----------------------
    # SUMMARY
    # -----------------------
    if active_tab == "Summary":
        st.markdown(result["summary"])

    # -----------------------
    # STEPS (FIXED)
    # -----------------------
    elif active_tab == "Steps":
        st.markdown("## 🔄 Workflow Diagram")
        
        mermaid_code = "graph TD\n"
        
        for i, step in enumerate(result["steps"], 1):
            # Clean string strictly to prevent Mermaid syntax errors
            clean = re.sub(r'^\d+\.\s*', '', step)
            # Streamlit's markdown parser converts `&` to `&amp;` which crashes Mermaid. Use `and`
            clean = clean.replace('"', "'").replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
            clean = clean.replace('&', 'and').replace('<', '').replace('>', '')
            
            # Since we now use pure JS Mermaid rendering, we can safely use HTML tags!
            # Wrap the full text every ~60 characters so it expands the box vertically
            import textwrap
            wrapped_text = "<br>".join(textwrap.wrap(clean, width=60))
            
            mermaid_code += f'    S{i}["<b>Step {i}:</b><br>{wrapped_text}"]\n'
            
            # Connect to previous node
            if i > 1:
                mermaid_code += f'    S{i-1} --> S{i}\n'
                
        # Removed classDef because custom CSS attributes like `border-radius:5px` can trigger syntax failure.
        
        import streamlit.components.v1 as components
        
        # Bypassing buggy Streamlit markdown and wrappers completely by forcing client-side JS rendering
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module">
              import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
              mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
            </script>
        </head>
        <body style="background-color: transparent;">
            <pre class="mermaid">
{mermaid_code}
            </pre>
        </body>
        </html>
        """
        components.html(html_code, height=600, scrolling=True)
        
        st.divider()
        with st.expander("Show Raw Text Steps"):
            for i, step in enumerate(result["steps"], 1):
                clean = re.sub(r'^\d+\.\s*', '', step)
                st.markdown(f"**Step {i}:** {clean}")

    # -----------------------
    # TRAINING
    # -----------------------
    elif active_tab == "Training":
        st.markdown(result["training_guide"])

    # -----------------------
    # QUIZ (FIXED)
    # -----------------------
    elif active_tab == "Quiz":
        quiz = result["quiz"]

        user_answers = []
        
        with st.form("quiz_form"):
            for i, q in enumerate(quiz, 1):
                st.markdown(f"### Q{i}. {q['question']}")

                labeled = []
                mapping = {}

                for idx, opt in enumerate(q["options"]):
                    # Clean any existing "A. ", "B. ", "A) ", etc from the option
                    clean_opt = re.sub(r'^[A-Za-z][\.\)]\s*', '', str(opt).strip())
                    letter = chr(65 + idx)
                    text = f"{letter}. {clean_opt}"
                    labeled.append(text)
                    mapping[text] = letter

                selected = st.radio("Select answer", labeled, key=f"q{i}")

                user_answers.append((selected, q["answer"], mapping))

            submitted = st.form_submit_button("Submit Quiz")
            
        if submitted:
            score = 0

            for i, (sel, correct, mapping) in enumerate(user_answers, 1):
                chosen = mapping[sel]
                correct_letter = str(correct).strip()[0].upper() # extract just 'A', 'B', etc safely

                if chosen == correct_letter:
                    st.success(f"Q{i}: Correct")
                    score += 1
                else:
                    st.error(f"Q{i}: Wrong | Correct Answer: {correct}")

            st.markdown(f"## Score: {score}/{len(user_answers)}")

    st.download_button(
        "Download JSON",
        json.dumps(result, indent=2),
        "output.json"
    )