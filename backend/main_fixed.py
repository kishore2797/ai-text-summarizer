from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Text Summarizer API",
    description="Advanced AI-powered text summarization with multiple models",
    version="1.0.0"
)

# CORS middleware - Fixed to include port 3002
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
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

# Simplified models for compatibility
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

# Basic summarization router (simplified)
@app.post("/api/v1/summarize/summarize", response_model=SummarizationResult)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize text using AI models (simplified version for Python 3.14 compatibility)
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
            },
            "advanced": {
                "name": "Advanced (Coming Soon)",
                "description": "Full AI models with transformers",
                "type": "abstractive",
                "max_input_length": 50000,
                "languages": ["english"],
                "best_for": "High-quality summaries",
                "status": "Coming soon - Python 3.14 compatibility update needed"
            }
        },
        "methods": {
            "extractive": {
                "name": "Extractive",
                "description": "Selects important sentences from original text",
                "speed": "Fast",
                "quality": "Good"
            },
            "abstractive": {
                "name": "Abstractive",
                "description": "Generates new sentences that capture the meaning",
                "speed": "Medium",
                "quality": "Excellent"
            },
            "hybrid": {
                "name": "Hybrid",
                "description": "Combines extractive and abstractive methods",
                "speed": "Medium",
                "quality": "Excellent"
            }
        }
    }

@app.get("/api/v1/summarize/health")
async def health_check():
    """
    Check the health of the summarization service
    """
    return {
        "status": "healthy",
        "models_loaded": True,
        "available_models": ["basic"],
        "service": "summarizer",
        "note": "Running in simplified mode for Python 3.14 compatibility"
    }

# File processing router (simplified)
@app.post("/api/v1/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a file (simplified version)
    """
    try:
        content = await file.read()
        
        # Basic text extraction based on file type
        if file.content_type == "text/plain":
            text = content.decode('utf-8')
        elif file.content_type == "application/pdf":
            text = f"PDF file uploaded: {file.filename}. Content extraction requires additional libraries."
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = f"DOCX file uploaded: {file.filename}. Content extraction requires additional libraries."
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "text_extracted": True,
            "text": text[:1000] + "..." if len(text) > 1000 else text,
            "statistics": {
                "word_count": len(text.split()),
                "character_count": len(text)
            },
            "language": "english"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@app.get("/api/v1/files/supported-formats")
async def get_supported_formats():
    """
    Get list of supported file formats and their limitations
    """
    return {
        "supported_formats": {
            "txt": {
                "mime_types": ["text/plain"],
                "max_size": "5MB",
                "description": "Plain text files"
            },
            "pdf": {
                "mime_types": ["application/pdf"],
                "max_size": "10MB",
                "description": "PDF documents (basic extraction)"
            },
            "docx": {
                "mime_types": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
                "max_size": "10MB",
                "description": "Microsoft Word documents (basic extraction)"
            }
        },
        "limitations": {
            "max_file_size": "10MB",
            "max_text_length": "100,000 characters",
            "supported_languages": ["english"]
        },
        "note": "Full file processing capabilities coming soon with Python 3.14 compatibility updates"
    }

# Export router (simplified)
class ExportRequest(BaseModel):
    content: str
    filename: Optional[str] = "summary"
    format: str
    include_metadata: Optional[bool] = False
    metadata: Optional[dict] = None

@app.post("/api/v1/export/export")
async def export_content(request: ExportRequest):
    """
    Export summary to various formats (simplified version)
    """
    try:
        if request.format == "txt":
            content = request.content
            if request.include_metadata and request.metadata:
                content += f"\n\n--- Metadata ---\n"
                for key, value in request.metadata.items():
                    content += f"{key}: {value}\n"
            
            from fastapi.responses import Response
            return Response(
                content=content,
                media_type="text/plain",
                headers={"Content-Disposition": f"attachment; filename={request.filename}.txt"}
            )
        else:
            return {
                "message": f"Export to {request.format} format coming soon",
                "current_format": "txt",
                "content": request.content
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/api/v1/export/formats")
async def get_export_formats():
    """
    Get available export formats and their features
    """
    return {
        "formats": {
            "txt": {
                "name": "TXT",
                "description": "Plain text format - universal compatibility",
                "features": ["Universal compatibility", "Small file size", "Simple format"],
                "mime_type": "text/plain",
                "available": True
            },
            "pdf": {
                "name": "PDF",
                "description": "Portable Document Format - best for sharing and printing",
                "features": ["Formatted layout", "Metadata support", "Professional appearance"],
                "mime_type": "application/pdf",
                "available": False,
                "status": "Coming soon"
            },
            "docx": {
                "name": "DOCX",
                "description": "Microsoft Word format - editable document",
                "features": ["Editable", "Metadata support", "Word processor compatible"],
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "available": False,
                "status": "Coming soon"
            }
        },
        "note": "Full export capabilities coming soon with Python 3.14 compatibility updates"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
