from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import time
import asyncio

from models.summarizer import (
    SummarizationRequest, 
    SummarizationResult, 
    BatchSummarizationRequest,
    BatchSummarizationResult
)
from services.summarizer_service import summarizer_service

router = APIRouter()

@router.post("/summarize", response_model=SummarizationResult)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize text using AI models
    
    - **text**: Text to summarize (minimum 50 characters)
    - **method**: Summarization method (extractive, abstractive, hybrid)
    - **model**: AI model to use (bart, t5, pegasus, openai, cohere)
    - **max_sentences**: Maximum number of sentences in summary
    - **max_length**: Maximum summary length in words
    - **min_length**: Minimum summary length in words
    """
    try:
        start_time = time.time()
        
        # Validate input
        if len(request.text.strip()) < 50:
            raise HTTPException(
                status_code=400, 
                detail="Text must be at least 50 characters long"
            )
        
        # Perform summarization
        if request.model == "openai":
            summary = await summarizer_service.summarize_with_openai(request.text, request)
        elif request.model == "cohere":
            summary = await summarizer_service.summarize_with_cohere(request.text, request)
        else:
            result = await summarizer_service.summarize_text(request)
            summary = result.summary
        
        processing_time = time.time() - start_time
        
        # Create result
        result = SummarizationResult(
            summary=summary,
            method=request.method,
            model=request.model,
            original_length=len(request.text.split()),
            summary_length=len(summary.split()),
            compression_ratio=len(summary.split()) / len(request.text.split()),
            processing_time=processing_time
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=BatchSummarizationResult)
async def batch_summarize(request: BatchSummarizationRequest):
    """
    Summarize multiple texts in a single request
    
    - **texts**: List of texts to summarize (1-10 texts)
    - Other parameters same as single summarization
    """
    try:
        start_time = time.time()
        results = []
        
        # Validate input
        if len(request.texts) > 10:
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 texts allowed per batch request"
            )
        
        # Process each text
        for i, text in enumerate(request.texts):
            if len(text.strip()) < 50:
                raise HTTPException(
                    status_code=400,
                    detail=f"Text {i+1} must be at least 50 characters long"
                )
            
            single_request = SummarizationRequest(
                text=text,
                method=request.method,
                model=request.model,
                max_sentences=request.max_sentences,
                max_length=request.max_length,
                min_length=request.min_length
            )
            
            if request.model == "openai":
                summary = await summarizer_service.summarize_with_openai(text, single_request)
            elif request.model == "cohere":
                summary = await summarizer_service.summarize_with_cohere(text, single_request)
            else:
                result = await summarizer_service.summarize_text(single_request)
                summary = result.summary
            
            processing_time = time.time() - start_time
            
            result = SummarizationResult(
                summary=summary,
                method=request.method,
                model=request.model,
                original_length=len(text.split()),
                summary_length=len(summary.split()),
                compression_ratio=len(summary.split()) / len(text.split()),
                processing_time=processing_time
            )
            
            results.append(result)
        
        total_processing_time = time.time() - start_time
        
        return BatchSummarizationResult(
            results=results,
            total_processing_time=total_processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_available_models():
    """
    Get list of available summarization models and their capabilities
    """
    return {
        "models": {
            "bart": {
                "name": "BART",
                "description": "Facebook's BART model for abstractive summarization",
                "type": "abstractive",
                "max_input_length": 1024,
                "languages": ["english"],
                "best_for": "General purpose summarization"
            },
            "t5": {
                "name": "T5",
                "description": "Google's T5 model for text-to-text tasks",
                "type": "abstractive",
                "max_input_length": 512,
                "languages": ["english"],
                "best_for": "Short to medium texts"
            },
            "pegasus": {
                "name": "PEGASUS",
                "description": "Google's PEGASUS model optimized for summarization",
                "type": "abstractive",
                "max_input_length": 1024,
                "languages": ["english"],
                "best_for": "Long documents and news articles"
            },
            "openai": {
                "name": "OpenAI GPT",
                "description": "OpenAI's GPT models for high-quality summarization",
                "type": "abstractive",
                "max_input_length": 4096,
                "languages": ["english", "spanish", "french", "german", "chinese"],
                "best_for": "High-quality, nuanced summaries",
                "requires_api_key": True
            },
            "cohere": {
                "name": "Cohere",
                "description": "Cohere's command model for summarization",
                "type": "abstractive",
                "max_input_length": 4096,
                "languages": ["english"],
                "best_for": "Business and technical documents",
                "requires_api_key": True
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

@router.get("/health")
async def health_check():
    """
    Check the health of the summarization service
    """
    try:
        # Test if models are loaded
        models_loaded = len(summarizer_service.models) > 0
        
        return {
            "status": "healthy" if models_loaded else "degraded",
            "models_loaded": models_loaded,
            "available_models": list(summarizer_service.models.keys()),
            "service": "summarizer"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "summarizer"
        }
