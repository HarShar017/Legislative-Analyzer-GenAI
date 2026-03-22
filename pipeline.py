from utils import chunk_text
from compressor import compress_text
from llm import generate_insights, format_insights


HIGH_VALUE_KEYWORDS = [
    "tax",
    "penalty",
    "mandatory",
    "increase",
    "decrease",
    "₹",
    "%",
]


def _is_high_value_chunk(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in HIGH_VALUE_KEYWORDS)


def _normalize_for_dedup(text: str) -> str:
    s = text.lower()
    cleaned_chars = []
    for ch in s:
        if ch.isalnum() or ch.isspace() or ch in {"%", "₹"}:
            cleaned_chars.append(ch)
    s = "".join(cleaned_chars)
    s = " ".join(s.split())
    return s


def _line_priority(line: str) -> int:
    score = 0
    if any(c.isdigit() for c in line) or "%" in line or "₹" in line:
        score += 3
    important_kw = ["increase", "decrease", "mandatory", "penalty", "fine", "tax", "deadline", "effective"]
    lower = line.lower()
    for kw in important_kw:
        if kw in lower:
            score += 2
    if len(line) > 120:
        score += 1
    return score


def refine_final_output(text: str) -> str:
    weak_phrases = [
        "this may affect",
        "various changes",
        "it is observed that",
        "this bill states that",
        "it may be noted that",
    ]
    leading_phrases = [
        "this bill states that ",
        "it is observed that ",
        "it may be noted that ",
    ]

    lines = [l.rstrip() for l in text.splitlines()]
    cleaned: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append("")
            continue
        if stripped.startswith("-"):
            content = stripped[1:].lstrip()
        else:
            content = stripped
        if len(content) < 20 and stripped.startswith("-"):
            continue
        low = content.lower()
        if any(p in low for p in weak_phrases):
            continue
        for p in leading_phrases:
            if low.startswith(p):
                content = content[len(p):].lstrip()
                break
        if len(content) > 200:
            content = content[:197].rstrip() + "..."
        if stripped.startswith("-"):
            cleaned.append("- " + content)
        else:
            cleaned.append(content)

    result_lines: list[str] = []
    seen_norm: list[str] = []
    for line in cleaned:
        if not line:
            result_lines.append("")
            continue
        norm = _normalize_for_dedup(line)
        is_duplicate = False
        for existing_norm in seen_norm:
            if existing_norm and norm and (norm in existing_norm or existing_norm in norm):
                is_duplicate = True
                break
        if is_duplicate:
            continue
        seen_norm.append(norm)
        result_lines.append(line)

    compact: list[str] = []
    prev_blank = False
    for line in result_lines:
        if not line.strip():
            if prev_blank:
                continue
            prev_blank = True
            compact.append("")
        else:
            prev_blank = False
            compact.append(line)

    return "\n".join(compact).rstrip("\n")


def structure_output(lines: list[str]) -> str:
    sections: dict[str, list[str]] = {
        "Key Changes": [],
        "Who is Affected": [],
        "Financial Impact": [],
        "Timeline": [],
        "Risks": [],
    }

    key_changes_kw = ["increase", "decrease", "amend", "change", "new", "introduce", "reform", "update", "modify"]
    who_kw = ["citizens", "students", "companies", "taxpayers", "individuals", "msme", "businesses", "workers", "households"]
    financial_kw = ["tax", "cost", "₹", "%", "penalty", "funding", "subsidy", "fee", "budget", "fine"]
    timeline_kw = ["year", "deadline", "effective", "from", "by", "within", "until", "start", "end", "date"]
    risks_kw = ["risk", "penalty", "fine", "violation", "issue", "concern", "uncertainty", "challenge"]

    for line in lines:
        lower = line.lower()
        scores = {
            "Key Changes": 0,
            "Who is Affected": 0,
            "Financial Impact": 0,
            "Timeline": 0,
            "Risks": 0,
        }

        for kw in key_changes_kw:
            if kw in lower:
                scores["Key Changes"] += 1
        for kw in who_kw:
            if kw in lower:
                scores["Who is Affected"] += 1
        for kw in financial_kw:
            if kw in lower:
                scores["Financial Impact"] += 1
        for kw in timeline_kw:
            if kw in lower:
                scores["Timeline"] += 1
        for kw in risks_kw:
            if kw in lower:
                scores["Risks"] += 1

        best_category = "Key Changes"
        best_score = 0
        for cat, sc in scores.items():
            if sc > best_score:
                best_score = sc
                best_category = cat

        sections[best_category].append(line)

    for key, items in sections.items():
        normalized_seen = set()
        deduped: list[str] = []
        for item in items:
            norm = _normalize_for_dedup(item)
            if norm in normalized_seen:
                continue
            normalized_seen.add(norm)
            deduped.append(item)
        deduped.sort(key=_line_priority, reverse=True)
        sections[key] = deduped

    parts: list[str] = []
    for header in ["Key Changes", "Who is Affected", "Financial Impact", "Timeline", "Risks"]:
        if not sections[header]:
            continue
        parts.append(f"{header}:")
        for item in sections[header]:
            # Remove leading bullet or dash if format_insights already added one
            clean_item = item.lstrip("•- ").strip()
            parts.append(f"- {clean_item}")
        parts.append("")

    return "\n".join(parts).rstrip("\n")


def run_pipeline(text: str):
    """
    Run the full legislative analysis pipeline on raw text.

    Stages:
    1. Chunk the text
    2. Filter invalid or very small chunks
    3. Compress each chunk
    4. Generate insights for each compressed chunk
    5. Aggregate all outputs into one clean string
    """
    if not text or not text.strip():
        return "", 0, 0, 0

    chunks = chunk_text(text)
    print(f"Chunks created: {len(chunks)}")

    filtered_chunks: list[str] = []
    for chunk in chunks:
        cleaned_chunk = chunk.strip()
        if not cleaned_chunk:
            continue
        if len(cleaned_chunk) < 100:
            continue
        filtered_chunks.append(cleaned_chunk)

    print(f"Chunks after filtering: {len(filtered_chunks)}")

    if not filtered_chunks:
        return "", len(filtered_chunks), 0, 0

    compressed_chunks: list[str] = []
    original_total_len = 0
    compressed_total_len = 0

    for chunk in filtered_chunks:
        original_total_len += len(chunk)
        if _is_high_value_chunk(chunk):
            compressed_result = compress_text(chunk)
            if isinstance(compressed_result, dict):
                compressed_text = str(compressed_result.get("compressed_text", "")).strip()
            else:
                compressed_text = str(compressed_result).strip()
        else:
            compressed_text = chunk[:500].strip()
        if compressed_text:
            compressed_chunks.append(compressed_text)
            compressed_total_len += len(compressed_text)

    print(f"Chunks after compression: {len(compressed_chunks)}")

    if original_total_len > 0 and compressed_total_len > 0:
        reduction_ratio = compressed_total_len / original_total_len
        reduction_pct = (1 - reduction_ratio) * 100
        print(
            f"Total compression: {original_total_len} → {compressed_total_len} "
            f"({reduction_ratio:.2f}x, {reduction_pct:.1f}% reduction)"
        )

    if not compressed_chunks:
        return "", len(filtered_chunks), original_total_len, compressed_total_len

    chunk_outputs: list[str] = []
    for compressed_text in compressed_chunks:
        insights_result = generate_insights(compressed_text)
        formatted_output = format_insights(insights_result)

        if formatted_output:
            chunk_outputs.append(formatted_output)

    print(f"Chunks after LLM stage: {len(chunk_outputs)}")

    if not chunk_outputs:
        return "", len(filtered_chunks), original_total_len, compressed_total_len

    all_lines: list[str] = []
    for output in chunk_outputs:
        for line in output.splitlines():
            cleaned_line = line.strip()
            if cleaned_line:
                all_lines.append(cleaned_line)

    unique_lines: list[str] = []
    seen_norm: set[str] = set()
    for line in all_lines:
        norm = _normalize_for_dedup(line)
        if norm in seen_norm:
            continue
        seen_norm.add(norm)
        unique_lines.append(line)

    structured = structure_output(unique_lines)
    final = refine_final_output(structured)
    return final, len(filtered_chunks), original_total_len, compressed_total_len


def process_document(text: str) -> dict:
    summary = ""
    try:
        result = run_pipeline(text)
        if isinstance(result, tuple) and len(result) == 4:
            summary, num_chunks, orig_chars, comp_chars = result
        elif isinstance(result, tuple) and len(result) == 2:
            summary, num_chunks = result
            orig_chars = len(text.split())
            comp_chars = int(orig_chars * 0.5)
        else:
            summary = result
            num_chunks = 0
            orig_chars = len(text.split())
            comp_chars = int(orig_chars * 0.5)
        status = "success"
    except Exception as e:
        status = f"error: {e}"
        num_chunks = 0
        orig_chars = len(text or "")
        comp_chars = 0
    return {
        "summary": summary,
        "num_chunks": num_chunks,
        "chunk_stats": {
            "original_total_tokens": orig_chars,
            "compressed_total_tokens": comp_chars,
        },
        "status": status,
    }
