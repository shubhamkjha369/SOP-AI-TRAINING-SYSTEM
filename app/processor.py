import re


def clean_text(text):
    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces but KEEP newlines
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove excessive empty lines
    text = re.sub(r'\n+', '\n', text)

    return text.strip()


def chunk_text(text, chunk_size=1200, overlap=200):
    if not text:
        return []

    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks


def structure_text(text):
    lines = text.split("\n")

    structured = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        # ✅ IMPROVED STEP DETECTION
        if (
            lower.startswith("step") or
            re.match(r'^\d+\.', line) or
            line.startswith("-") or
            line.startswith("*")
        ):
            structured.append(f"[STEP] {line}")
        else:
            structured.append(f"[INFO] {line}")

    return "\n".join(structured)