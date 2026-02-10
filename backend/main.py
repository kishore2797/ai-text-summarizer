from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Text Summarizer API",
    description="Advanced AI-powered text summarization with multiple models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Initialize database (simplified for now)
    print("🚀 AI Text Summarizer API starting up...")

@app.get("/")
async def root():
    return {
        "message": "AI Text Summarizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-summarizer"}

class SummarizationRequest(BaseModel):
    text: str
    method: str = "extractive"
    model: str = "basic"
    max_sentences: int = 5
    max_length: int = 150
    min_length: int = 50

class SummarizationResult(BaseModel):
    summary: str
    method: str
    model: str
    original_length: int
    summary_length: int
    compression_ratio: float
    processing_time: float

        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-summarizer"}

@app.post("/api/v1/summarize/summarize", response_model=SummarizationResult)
async def summarize_text(request: SummarizationRequest):
    """
    Simple text summarization for demonstration
    """
    try:
        import time
        import re
        
        start_time = time.time()
        
        # Basic extractive summarization
        text = request.text.strip()
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= request.max_sentences:
            summary = text
        else:
            # Simple extractive: take first N sentences
            summary = '. '.join(sentences[:request.max_sentences]) + '.'
        
        # Ensure summary length constraints
        summary_words = summary.split()
        if len(summary_words) > request.max_length:
            summary = ' '.join(summary_words[:request.max_length])
        
        processing_time = time.time() - start_time
        
        return SummarizationResult(
            summary=summary,
            method=request.method,
            model=request.model,
            original_length=len(words),
            summary_length=len(summary_words),
            compression_ratio=len(summary_words) / len(words) if len(words) > 0 else 0,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.get("/api/v1/summarize/models")
async def get_available_models():
    """
    Get list of available summarization models
    """
    return {
        "models": {
            "basic": {
                "name": "Basic Extractive",
                "description": "Simple extractive summarization for demonstration",
                "type": "extractive",
                "max_input_length": 10000,
                "languages": ["english"],
                "best_for": "Quick demonstrations and testing"
            }
        },
        "methods": {
            "extractive": {
                "name": "Extractive",
                "description": "Selects important sentences from original text",
                "speed": "Fast",
                "quality": "Good"
            }
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
