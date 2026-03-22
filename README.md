"# AI Legislative Analyzer 🏛️

A minimal but fully functional FastAPI-based system for analyzing large legislative documents using multi-step AI pipelines with token compression.

## Overview

This project demonstrates a complete end-to-end solution for:

1. **Document Ingestion** - Upload PDFs or paste text
2. **Intelligent Chunking** - Split documents into manageable pieces
3. **Token Compression** - Reduce token count using ScaleDown
4. **LLM Analysis** - Generate structured insights (key changes, impacts, timeline, risks)
5. **Aggregation** - Combine insights across all chunks

## Project Structure

```
Legislative-Analyzer-GenAI/
├── app.py                 # FastAPI main application
├── pipeline.py            # Main processing pipeline orchestrator
├── compressor.py          # ScaleDown token compression
├── parser.py              # PDF and text extraction
├── llm.py                 # LLM integration (mock + formatting)
├── utils.py               # Chunking and utility functions
├── requirements.txt       # Python dependencies
└── frontend/
    └── index.html         # Simple web UI
```

## Features

### ✨ Core Capabilities

- **Multi-format Input**: Upload PDF files or paste raw text
- **Smart Chunking**: Intelligent text splitting with overlap handling
- **Token Compression**: ScaleDown-based compression for efficient processing
- **Structured Insights**: Extract key changes, affected parties, financial impacts, timelines, and risks
- **Compression Statistics**: Track token reduction across the pipeline
- **Clean, Modular Code**: Well-documented functions with minimal complexity

### 🎨 Frontend

- Modern, responsive HTML/CSS UI
- Tab-based input (text/file)
- Real-time compression statistics
- Formatted analysis output with bullet points
- Drag-and-drop file upload

### 🔧 Backend

- FastAPI REST API with async support
- PDF parsing with pypdf
- Clean separation of concerns
- Comprehensive logging and progress tracking
- Error handling with meaningful messages

## Installation

### 1. Clone or extract the project

```bash
cd Legislative-Analyzer-GenAI
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Server

```bash
python app.py
```

You should see:

```
============================================================
🚀 AI LEGISLATIVE ANALYZER
============================================================

📌 Starting server...
   Access the app at: http://127.0.0.1:8000
   API docs at: http://127.0.0.1:8000/docs

============================================================
```

### Access the Application

- **Web UI**: Open your browser to `http://127.0.0.1:8000`
- **API Docs**: `http://127.0.0.1:8000/docs` (Swagger UI)

## Usage

### Using the Web UI

1. **Paste Text**:
   - Click the "📝 Paste Text" tab
   - Paste your legislative document
   - Click "🚀 Analyze Document"

2. **Upload File**:
   - Click the "📤 Upload File" tab
   - Drag and drop a PDF or text file (or click to browse)
   - Click "🚀 Analyze Document"

3. **View Results**:
   - See compression statistics
   - Read formatted analysis with:
     - Key Changes
     - Who is Affected
     - Financial/Legal Impact
     - Timeline
     - Risks/Concerns

### Using the API

#### Request

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf"
```

Or with text:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "text=Your legal document text here..."
```

#### Response

```json
{
  "summary": "KEY CHANGES:\n• Legislative amendments identified\n...",
  "num_chunks": 5,
  "chunk_stats": {
    "original_total_tokens": 2500,
    "compressed_total_tokens": 1850,
    "chunks_processed": 5
  },
  "status": "success"
}
```

## Pipeline Stages

### Stage 1: Text Cleaning
- Normalizes whitespace
- Prepares text for chunking

### Stage 2: Chunking
- Splits text into ~2000 character chunks
- Maintains overlap for context (200 chars)
- Filters out very small chunks
- Tries to break at sentence boundaries

### Stage 3: Compression
- Uses ScaleDown compressor on each chunk
- Tracks token reduction per chunk
- Falls back gracefully if ScaleDown unavailable
- Displays overall compression percentage

### Stage 4: Insight Generation
- Pattern-based analysis (mock LLM)
- Extracts 5 categories of insights:
  - **Key Changes**: amendments, new provisions
  - **Who Affected**: citizens, businesses, government
  - **Financial Impact**: costs, fees, penalties
  - **Timeline**: implementation dates, effective dates
  - **Risks/Concerns**: compliance issues, potential problems

### Stage 5: Aggregation
- Combines insights from all chunks
- Removes duplicates
- Formats as bullet-pointed text

## Configuration

### Adjust Chunk Size

In `pipeline.py`, modify the `chunk_text()` call:

```python
chunks = chunk_text(text, chunk_size=3000, overlap=300)
```

### Use Real LLM API

In `llm.py`, replace the mock `generate_insights()` function with actual API calls:

```python
import openai

def generate_insights(chunk: str) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract legal insights..."},
            {"role": "user", "content": chunk}
        ]
    )
    # Parse and structure response...
```

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **python-multipart** - File upload handling
- **pydantic** - Data validation
- **pypdf** - PDF text extraction
- **scaledown** - Token compression

## Key Code Examples

### Run the Pipeline

```python
from pipeline import process_document

result = process_document(your_text)
print(result['summary'])
print(f"Chunks: {result['num_chunks']}")
```

### Extract PDF Text

```python
from parser import extract_text_from_pdf

with open('law.pdf', 'rb') as f:
    text = extract_text_from_pdf(f.read())
```

### Compress Text

```python
from compressor import compress_chunk

compressed, stats = compress_chunk(text_chunk)
print(f"Compression: {stats['compression_ratio']:.0%}")
```

## Logs and Progress

The application prints detailed progress at each stage:

```
============================================================
STARTING DOCUMENT ANALYSIS PIPELINE
============================================================

[1/5] Cleaning text...
    ✓ Text cleaned (15432 characters)

[2/5] Chunking document...
    ✓ Created 8 chunks

[3/5] Compressing chunks with ScaleDown...
    ✓ Chunk 1/8 compressed 35.2%
    ✓ Chunk 2/8 compressed 38.1%
    ...
    Overall compression: 36.5%

[4/5] Generating insights from compressed chunks...
    ✓ Insights generated for chunk 1/8
    ...

[5/5] Aggregating results...
    ✓ Aggregation complete

============================================================
ANALYSIS COMPLETE
============================================================
```

## Extending the System

### Add Database Storage

Replace in-memory results with a database (SQLite, PostgreSQL):

```python
from sqlalchemy import create_engine
# Add model and store results
```

### Add Authentication

Protect the API with API keys or OAuth2:

```python
from fastapi.security import HTTPBearer
```

### Use Real LLM APIs

Replace mock insights with:
- OpenAI GPT-4
- Anthropic Claude
- LLaMA via Ollama
- Local fine-tuned models

### Add Email Notifications

Send analysis results via email:

```python
import smtplib
```

### Implement Caching

Cache analysis results for identical documents:

```python
from functools import lru_cache
```

## Troubleshooting

### "ScaleDown not available" warning

If you see this, ScaleDown isn't installed. The system will still work with original chunks.

```bash
pip install scaledown
```

### PDF extraction issues

Ensure the PDF has extractable text (not scanned images):

```bash
pip install --upgrade pypdf
```

### Port already in use

Change the port in `app.py`:

```python
uvicorn.run(app, host="127.0.0.1", port=8001)
```

## Performance Tips

- **Large documents**: Increase chunk size to reduce overhead
- **Many chunks**: Implement batching for parallel processing
- **Memory constraints**: Stream processing instead of loading all at once
- **API rate limits**: Add request queuing/throttling

## License

Open source - MIT License

## Next Steps

- [ ] Replace mock LLM with real API integration
- [ ] Add database for storing analysis history
- [ ] Implement user authentication
- [ ] Add support for multiple languages
- [ ] Build admin dashboard for analytics
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Add WebSocket support for real-time updates
- [ ] Create Docker containerization

---

**Built with ❤️ for legislative analysis | 2026**
" 
