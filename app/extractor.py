import fitz  # PyMuPDF


def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""

        for page in doc:
            page_text = page.get_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print("PDF extraction error:", e)
        return ""


def extract_text(input_file):
    if input_file is None:
        return ""

    try:
        input_file.seek(0)  # reset pointer

        # 🔹 PDF handling
        if input_file.type == "application/pdf":
            text = extract_text_from_pdf(input_file)

        # 🔹 Text / other files
        else:
            content = input_file.read()

            if isinstance(content, bytes):
                text = content.decode("utf-8", errors="ignore")
            else:
                text = str(content)

        # 🔹 Final cleanup (light)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        return text.strip()

    except Exception as e:
        print("Extraction error:", e)
        return ""