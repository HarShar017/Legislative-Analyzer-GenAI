import re


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:
    chunks = []
    text = re.sub(r'\s+', ' ', text).strip()
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            last_period = text.rfind('. ', start, end)
            if last_period != -1:
                end = last_period + 2
            else:
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and last_space > start:
                    end = last_space + 1
        chunk = text[start:end].strip()
        if chunk and len(chunk) > 50:
            chunks.append(chunk)
        start = end - overlap if end < len(text) else end
    return chunks


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_duplicates(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
