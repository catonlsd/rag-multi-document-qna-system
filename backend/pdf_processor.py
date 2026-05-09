import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    pages_text = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        pages_text.append({
            "page_number": page_num,
            "text": text
        })

    doc.close()
    return pages_text