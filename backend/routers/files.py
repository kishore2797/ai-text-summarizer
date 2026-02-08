from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
import tempfile
import aiofiles
from utils.text_processor import TextProcessor

router = APIRouter()
text_processor = TextProcessor()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    extract_text: bool = Form(True)
):
    """
    Upload and process a file (PDF, DOCX, TXT)
    
    - **file**: File to upload (PDF, DOCX, or TXT)
    - **extract_text**: Whether to extract text from the file
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Allowed types: PDF, DOCX, TXT"
            )
        
        # Read file content
        content = await file.read()
        
        if not extract_text:
            return {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "text_extracted": False
            }
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            text = text_processor.extract_text_from_pdf(content)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = text_processor.extract_text_from_docx(content)
        elif file.content_type == "text/plain":
            text = text_processor.extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Get text statistics
        stats = text_processor.get_text_statistics(text)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "text_extracted": True,
            "text": text,
            "statistics": stats,
            "language": text_processor.detect_language(text)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@router.post("/process-text")
async def process_text(text: str):
    """
    Process raw text and return statistics and preprocessing results
    
    - **text**: Raw text to process
    """
    try:
        if len(text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters long"
            )
        
        # Preprocess text
        processed_text = text_processor.preprocess_text(text)
        
        # Get statistics
        stats = text_processor.get_text_statistics(processed_text)
        
        # Detect language
        language = text_processor.detect_language(processed_text)
        
        return {
            "original_text": text,
            "processed_text": processed_text,
            "statistics": stats,
            "language": language,
            "is_suitable_for_summarization": stats["word_count"] >= 50
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text processing failed: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported file formats and their limitations
    """
    return {
        "supported_formats": {
            "pdf": {
                "mime_types": ["application/pdf"],
                "max_size": "10MB",
                "description": "PDF documents with extractable text"
            },
            "docx": {
                "mime_types": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
                "max_size": "10MB",
                "description": "Microsoft Word documents"
            },
            "txt": {
                "mime_types": ["text/plain"],
                "max_size": "5MB",
                "description": "Plain text files"
            }
        },
        "limitations": {
            "max_file_size": "10MB",
            "max_text_length": "100,000 characters",
            "supported_languages": ["english", "spanish", "french"]
        },
        "recommendations": {
            "best_format": "TXT for direct text input",
            "for_documents": "PDF or DOCX for formatted documents",
            "language_support": "Best results with English text"
        }
    }
