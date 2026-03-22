from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path

from pipeline import process_document
from parser import extract_text_from_pdf, extract_text_from_raw


class ChunkStats(BaseModel):
    original_total_tokens: int = 0
    compressed_total_tokens: int = 0


class AnalyzeResponse(BaseModel):
    status: str
    summary: Optional[str] = ""
    num_chunks: Optional[int] = 0
    chunk_stats: Optional[ChunkStats] = None
    error: Optional[str] = None


app = FastAPI(
    title="AI Legislative Analyzer",
    description="Analyze legislative documents with AI-powered insights",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    frontend_path = BASE_DIR / "frontend" / "index.html"
    if frontend_path.exists():
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Frontend not found</h1>"


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(
    file: UploadFile = None,
    text: str = Form(None)
):
    try:
        extracted_text = None
        if file:
            content = await file.read()
            if file.filename.lower().endswith('.pdf'):
                print(f"\n📄 Processing PDF: {file.filename}")
                extracted_text = extract_text_from_pdf(content)
            else:
                print(f"\n📄 Processing text file: {file.filename}")
                extracted_text = content.decode('utf-8')
        elif text:
            print("\n📝 Processing raw text input")
            extracted_text = extract_text_from_raw(text)
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": "No input provided. Please upload a file or paste text.",
                    "summary": "",
                    "num_chunks": 0,
                    "chunk_stats": {
                        "original_total_tokens": 0,
                        "compressed_total_tokens": 0
                    }
                }
            )
        if not extracted_text or len(extracted_text.strip()) == 0:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": "Could not extract any text from the input.",
                    "summary": "",
                    "num_chunks": 0,
                    "chunk_stats": {
                        "original_total_tokens": 0,
                        "compressed_total_tokens": 0
                    }
                }
            )
        result = process_document(extracted_text)

        # Guarantee all fields exist and have correct types
        summary = result.get("summary") or ""
        num_chunks = result.get("num_chunks") or 0
        chunk_stats = result.get("chunk_stats") or {}

        safe_response = {
            "status": "success",
            "summary": str(summary),
            "num_chunks": int(num_chunks),
            "chunk_stats": {
                "original_total_tokens": int(
                    chunk_stats.get("original_total_tokens") or 0
                ),
                "compressed_total_tokens": int(
                    chunk_stats.get("compressed_total_tokens") or 0
                )
            }
        }

        return JSONResponse(
            status_code=200,
            content=safe_response
        )
    except Exception as e:
        import traceback
        print(f"\n❌ Error during analysis: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": f"Analysis failed: {str(e)}",
                "summary": "",
                "num_chunks": 0,
                "chunk_stats": {
                    "original_total_tokens": 0,
                    "compressed_total_tokens": 0
                }
            }
        )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Legislative Analyzer"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 AI LEGISLATIVE ANALYZER")
    print("="*60)
    print("\n📌 Starting server...")
    print("   Access the app at: http://127.0.0.1:8000")
    print("   API docs at: http://127.0.0.1:8000/docs")
    print("\n" + "="*60 + "\n")

    print("\n🔍 Verifying pipeline imports...")
    try:
        from pipeline import process_document
        from parser import extract_text_from_pdf, extract_text_from_raw
        print("✅ All pipeline imports successful")
    except Exception as e:
        print(f"❌ Pipeline import failed: {e}")
        import traceback
        print(traceback.format_exc())

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
