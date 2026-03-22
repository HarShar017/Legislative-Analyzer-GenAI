import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"


def _fallback_compress(chunk: str) -> dict:
    chunk = chunk.strip()
    if not chunk:
        return {
            "compressed_text": "",
            "original_length": 0,
            "compressed_length": 0,
        }
    original_length = len(chunk)
    compressed_text = chunk[:800]
    compressed_length = len(compressed_text)
    return {
        "compressed_text": compressed_text,
        "original_length": original_length,
        "compressed_length": compressed_length,
    }


def compress_text(chunk: str) -> dict:
    if not chunk or not isinstance(chunk, str):
        return {
            "compressed_text": "",
            "original_length": 0,
            "compressed_length": 0,
        }
    chunk = chunk.strip()
    if not chunk:
        return {
            "compressed_text": "",
            "original_length": 0,
            "compressed_length": 0,
        }
    if not SCALEDOWN_API_KEY:
        return _fallback_compress(chunk)
    payload = {
        "context": "Extract only key legal actions, affected entities, and financial or policy impacts. Remove boilerplate and repetition.",
        "prompt": chunk,
        "model": "gpt-4o",
        "scaledown": {
            "rate": "auto",
        },
    }
    try:
        response = requests.post(
            SCALEDOWN_URL,
            headers={
                "x-api-key": SCALEDOWN_API_KEY,
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            timeout=30,
        )
        if response.status_code != 200:
            return _fallback_compress(chunk)
        data = response.json() or {}
        compressed_text = (
            data.get("compressed_text")
            or data.get("compressed")
            or data.get("output")
            or data.get("result")
            or chunk[:800]
        )
        compressed_text = str(compressed_text).strip()
        original_length = len(chunk)
        compressed_length = len(compressed_text)
        return {
            "compressed_text": compressed_text,
            "original_length": original_length,
            "compressed_length": compressed_length,
        }
    except Exception:
        return _fallback_compress(chunk)
