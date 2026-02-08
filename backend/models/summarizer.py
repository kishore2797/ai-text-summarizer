from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class SummarizationMethod(str, Enum):
    EXTRACTIVE = "extractive"
    ABSTRACTIVE = "abstractive"
    HYBRID = "hybrid"

class SummarizationModel(str, Enum):
    BART = "bart"
    T5 = "t5"
    PEGASUS = "pegasus"
    OPENAI = "openai"
    COHERE = "cohere"

class SummarizationRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize")
    method: SummarizationMethod = Field(default=SummarizationMethod.HYBRID, description="Summarization method")
    model: SummarizationModel = Field(default=SummarizationModel.BART, description="AI model to use")
    max_sentences: int = Field(default=5, ge=1, le=20, description="Maximum number of sentences")
    max_length: int = Field(default=150, ge=50, le=500, description="Maximum summary length in words")
    min_length: int = Field(default=50, ge=10, le=200, description="Minimum summary length in words")
    language: str = Field(default="english", description="Language of the text")
    
    class Config:
        use_enum_values = True

class SummarizationResult(BaseModel):
    summary: str = Field(..., description="Generated summary")
    method: SummarizationMethod = Field(..., description="Method used")
    model: SummarizationModel = Field(..., description="Model used")
    original_length: int = Field(..., description="Original text length in words")
    summary_length: int = Field(..., description="Summary length in words")
    compression_ratio: float = Field(..., description="Compression ratio (summary/original)")
    processing_time: float = Field(..., description="Processing time in seconds")
    
    class Config:
        use_enum_values = True

class BatchSummarizationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=10, description="List of texts to summarize")
    method: SummarizationMethod = Field(default=SummarizationMethod.HYBRID)
    model: SummarizationModel = Field(default=SummarizationModel.BART)
    max_sentences: int = Field(default=5, ge=1, le=20)
    max_length: int = Field(default=150, ge=50, le=500)
    min_length: int = Field(default=50, ge=10, le=200)
    
    class Config:
        use_enum_values = True

class BatchSummarizationResult(BaseModel):
    results: List[SummarizationResult] = Field(..., description="List of summarization results")
    total_processing_time: float = Field(..., description="Total processing time")
    
    class Config:
        use_enum_values = True
