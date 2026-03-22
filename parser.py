import re
from io import BytesIO
from pypdf import PdfReader


def clean_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([.,;:!?])", r"\1", text)
    text = text.strip()
    return text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not file_bytes or not isinstance(file_bytes, bytes):
        raise ValueError("Invalid input: file_bytes must be non-empty bytes. Ensure a valid PDF file was uploaded.")
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                pages.append(text)
        except Exception as e:
            print(f"WARNING: Could not extract page {i + 1}: {e}")
            continue
    if not pages:
        raise ValueError("PDF appears to be empty or contains no extractable text. Scanned PDFs require OCR which is not supported.")
    combined = " ".join(pages)
    return clean_text(combined)


def extract_text_from_raw(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    return clean_text(text)
