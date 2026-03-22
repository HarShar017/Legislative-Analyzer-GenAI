import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment")

try:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = client
    GENAI_MODE = "new"
    print("Gemini model initialized successfully")
except ImportError:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        GENAI_MODE = "legacy"
        print("Gemini model initialized successfully (legacy mode)")
    except Exception as e:
        model = None
        GENAI_MODE = None
        print(f"WARNING: Gemini model initialization failed: {e}")
except Exception as e:
    model = None
    GENAI_MODE = None
    print(f"WARNING: Gemini model initialization failed: {e}")

INSIGHT_PROMPT_TEMPLATE = """
Analyze the following legal or policy text and extract 
only high-value insights.

CRITICAL INSTRUCTION: Your response must start with {{ and 
end with }}. Output ONLY the JSON object. No introduction.
No explanation. No preamble. No markdown. No code blocks.
The very first character of your response must be {{.
The very last character of your response must be }}.

JSON structure to fill:
{{
  "key_changes": [],
  "who_affected": [],
  "financial_impact": [],
  "timeline": [],
  "risks_concerns": []
}}

Rules:
- Max 6 items per category
- Each item must be 5 to 12 words
- Prefer numbers, percentages, deadlines, specific actions
- No generic statements
- If no info for a category: ["No specific information found"]
- Never return empty lists

Text to analyze:
{input_text}
"""


def generate_insights(text: str) -> dict:
    EMPTY_RESULT = {
        "key_changes": ["Unable to extract insights"],
        "who_affected": ["Unable to determine"],
        "financial_impact": ["Unable to determine"],
        "timeline": ["Unable to determine"],
        "risks_concerns": ["Unable to determine"],
    }

    if not text or not isinstance(text, str):
        print("WARNING: Invalid input to generate_insights")
        return EMPTY_RESULT

    text = text.strip()
    if len(text) == 0:
        print("WARNING: Empty text received")
        return EMPTY_RESULT

    if model is None:
        print("WARNING: Gemini model not available")
        return EMPTY_RESULT

    raw = ""
    try:
        prompt = INSIGHT_PROMPT_TEMPLATE.format(input_text=text)
        # Call Gemini based on which package is available
        if GENAI_MODE == "new":
            from google.genai import types
            response = model.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    max_output_tokens=1500
                )
            )
            raw = response.text.strip()
        elif GENAI_MODE == "legacy":
            generation_config = {
                "temperature": 0.0,
                "max_output_tokens": 1500
            }
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            raw = response.text.strip()
        else:
            print("WARNING: Gemini model not available")
            return EMPTY_RESULT

        print(f"[Gemini] Raw response length: {len(raw)} characters")
        print(f"[Gemini] First 100 chars: {raw[:100]}")

        # Strip markdown code blocks if present
        if "```" in raw:
            raw = re.sub(r"```(?:json)?\n?", "", raw)
            raw = raw.replace("```", "").strip()

        start_idx = raw.find("{")
        end_idx = raw.rfind("}")

        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            print("WARNING: No valid JSON object found in response")
            print(f"[Gemini] Full raw output: {raw[:500]}")
            return EMPTY_RESULT

        # Extract only the JSON portion
        json_str = raw[start_idx:end_idx + 1]
        print(f"[Gemini] Extracted JSON length: {len(json_str)} characters")

        # Parse the extracted JSON
        insights = json.loads(json_str)

        required_keys = [
            "key_changes",
            "who_affected",
            "financial_impact",
            "timeline",
            "risks_concerns",
        ]

        for key in required_keys:
            if key not in insights:
                insights[key] = ["Not specified"]
            elif not isinstance(insights[key], list):
                insights[key] = [str(insights[key])]

            if len(insights[key]) == 0:
                insights[key] = ["No specific information found"]

        print("[Gemini] Insights extracted successfully")
        print(f"[Gemini] Categories returned: {list(insights.keys())}")

        return insights
    except json.JSONDecodeError as e:
        print(f"WARNING: JSON parsing failed: {e}")
        print(f"[Gemini] Raw output was: {raw[:200]}")
        return EMPTY_RESULT
    except Exception as e:
        print(f"WARNING: Gemini call failed: {e}")
        return EMPTY_RESULT


def format_insights(insights: dict) -> str:
    LABELS = {
        "key_changes": "Key Changes",
        "who_affected": "Who Is Affected",
        "financial_impact": "Financial Impact",
        "timeline": "Timeline",
        "risks_concerns": "Risks and Concerns",
    }

    lines = []

    for key in [
        "key_changes",
        "who_affected",
        "financial_impact",
        "timeline",
        "risks_concerns",
    ]:
        lines.append(f"\n{LABELS[key]}")
        lines.append("-" * len(LABELS[key]))

        items = insights.get(key, ["Not available"])

        if not isinstance(items, list):
            items = [str(items)]

        for item in items:
            lines.append(f"  • {str(item).strip()}")

    return "\n".join(lines).strip()
