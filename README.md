# AI Legislative Analyzer

FastAPI + React application for analyzing legislative and policy documents using chunking, compression, and LLM-powered insight extraction.

## Current Stack

- Backend: FastAPI, Uvicorn
- LLM: Google Gemini (`google-generativeai`)
- Compression: ScaleDown API with fallback compression
- Parsing: `pypdf` for PDF extraction
- Frontend: React 18 + Vite + Tailwind CSS + Framer Motion + Lucide React + Axios

## Repository Structure

```text
Legislative-Analyzer-GenAI/
├── app.py
├── pipeline.py
├── compressor.py
├── llm.py
├── parser.py
├── utils.py
├── test_pipeline.py
├── requirements.txt
├── .env
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        └── components/
            ├── Navbar.jsx
            ├── Hero.jsx
            ├── AnalysisCard.jsx
            ├── TextTab.jsx
            ├── FileTab.jsx
            ├── StatsRow.jsx
            ├── ResultsCard.jsx
            └── InsightSection.jsx
```

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm 9+

## Environment Variables

Create `.env` in the repository root:

```env
GEMINI_API_KEY=your_gemini_api_key
SCALEDOWN_API_KEY=your_scaledown_api_key
```

Notes:
- `GEMINI_API_KEY` is required for LLM insights.
- If `SCALEDOWN_API_KEY` is missing, the app still works using fallback compression.

## Installation

### 1) Backend setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Frontend setup

```bash
cd frontend
npm install
cd ..
```

## Running the Project

Run backend and frontend in separate terminals.

### Terminal 1: Backend

```bash
source .venv/bin/activate
python app.py
```

Backend runs at:
- API base: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at:
- App: `http://localhost:5173`

Vite proxy forwards:
- `/analyze` -> `http://127.0.0.1:8000/analyze`
- `/health` -> `http://127.0.0.1:8000/health`

## API Usage

### `POST /analyze`

Accepts either:
- `file` (multipart upload; PDF or text)
- `text` (form field)

Example (file):

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf"
```

Example (raw text):

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "text=Your policy or bill text here"
```

Example response:

```json
{
  "status": "success",
  "summary": "Key Changes:\n- ...",
  "num_chunks": 4,
  "chunk_stats": {
    "original_total_tokens": 8400,
    "compressed_total_tokens": 3100
  }
}
```

## Implementation Flow

### 1) Input parsing (`app.py`, `parser.py`)
- Detects PDF vs text input
- Extracts and cleans text
- Rejects empty/unreadable input

### 2) Chunking (`utils.py`)
- Splits text into chunks (default 2000 chars)
- Uses overlap (default 200 chars)
- Tries sentence/word boundaries

### 3) Compression (`compressor.py`)
- Attempts ScaleDown compression
- Falls back to deterministic local compression if API is unavailable

### 4) Insight generation (`llm.py`)
- Sends compressed chunk text to Gemini
- Enforces strict JSON response shape
- Formats into 5 sections:
  - Key Changes
  - Who Is Affected
  - Financial Impact
  - Timeline
  - Risks and Concerns

### 5) Aggregation and refinement (`pipeline.py`)
- Deduplicates and prioritizes lines
- Re-structures final output into sectioned bullets
- Returns chunk stats and final summary

## Frontend Features

- Two input modes: text and file upload
- Animated tab switching and transitions
- Analyze button with loading state
- Error handling UI
- Parsed result rendering by sections
- Stats cards:
  - Chunks Processed
  - Original Tokens
  - Compressed Tokens
  - Compression Rate

## Testing

Run the sample pipeline test:

```bash
source .venv/bin/activate
python test_pipeline.py
```

This runs the end-to-end backend pipeline using the sample legislative text in `test_pipeline.py`.

## Build Frontend

```bash
cd frontend
npm run build
npm run preview
```

## Troubleshooting

### Missing Gemini key
Symptom: warnings about Gemini model not available and weak/no insights.
Fix: set `GEMINI_API_KEY` in `.env`.

### ScaleDown unavailable
Symptom: compression still works but uses fallback behavior.
Fix: set `SCALEDOWN_API_KEY` in `.env`.

### Empty PDF extraction
Symptom: "contains no extractable text" error.
Fix: use text-based PDFs (scanned/image PDFs need OCR, not implemented here).

### Port conflicts
- Backend port is configured in `app.py` (`8000`)
- Frontend dev server defaults to `5173`

## Important Notes

- Main user interface is the React app served by Vite at `http://localhost:5173` during development.
- Backend remains API-first and serves `/analyze`, `/health`, and Swagger docs.
