import asyncio
from typing import Dict, List, Optional
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import openai
import cohere
from models.summarizer import SummarizationRequest, SummarizationResult
from utils.text_processor import TextProcessor

class SummarizerService:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load all available summarization models"""
        try:
            # BART model for abstractive summarization
            self.models['bart'] = pipeline(
                "text2text-generation",
                model="facebook/bart-large-cnn",
                tokenizer="facebook/bart-large-cnn"
            )
            
            # T5 model for multiple tasks
            self.models['t5'] = pipeline(
                "text2text-generation",
                model="t5-base",
                tokenizer="t5-base"
            )
            
            # PEGASUS model for long documents
            self.models['pegasus'] = pipeline(
                "text2text-generation",
                model="google/pegasus-cnn_dailymail",
                tokenizer="google/pegasus-cnn_dailymail"
            )
            
            # Sentence embeddings for extractive summarization
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # spaCy not available with Python 3.14, using NLTK instead
            self.nlp = None
                
        except Exception as e:
            print(f"Error loading models: {e}")
    
    async def summarize_text(self, request: SummarizationRequest) -> SummarizationResult:
        """Main summarization method"""
        try:
            # Preprocess text
            processed_text = self.text_processor.preprocess_text(request.text)
            
            # Choose summarization method
            if request.method == "extractive":
                summary = await self._extractive_summarize(processed_text, request)
            elif request.method == "abstractive":
                summary = await self._abstractive_summarize(processed_text, request)
            else:
                # Hybrid approach (default)
                summary = await self._hybrid_summarize(processed_text, request)
            
            # Calculate metrics
            original_length = len(request.text.split())
            summary_length = len(summary.split())
            compression_ratio = summary_length / original_length if original_length > 0 else 0
            
            return SummarizationResult(
                summary=summary,
                method=request.method,
                model=request.model,
                original_length=original_length,
                summary_length=summary_length,
                compression_ratio=compression_ratio,
                processing_time=0  # Will be set by the router
            )
            
        except Exception as e:
            raise Exception(f"Summarization failed: {str(e)}")
    
    async def _extractive_summarize(self, text: str, request: SummarizationRequest) -> str:
        """Extractive summarization using sentence embeddings"""
        try:
            # Split text into sentences using NLTK
            sentences = nltk.sent_tokenize(text)
            
            if len(sentences) <= request.max_sentences:
                return text
            
            # Calculate sentence embeddings
            embeddings = self.sentence_model.encode(sentences)
            
            # Calculate sentence importance scores
            scores = self._calculate_sentence_scores(embeddings)
            
            # Select top sentences
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:request.max_sentences]
            top_indices.sort()  # Maintain original order
            
            summary_sentences = [sentences[i] for i in top_indices]
            return '. '.join(summary_sentences)
            
        except Exception as e:
            raise Exception(f"Extractive summarization failed: {str(e)}")
    
    async def _abstractive_summarize(self, text: str, request: SummarizationRequest) -> str:
        """Abstractive summarization using transformer models"""
        try:
            model = self.models.get(request.model, self.models['bart'])
            
            # Handle long texts by chunking
            max_chunk_length = 1024
            if len(text) > max_chunk_length:
                chunks = self.text_processor.chunk_text(text, max_chunk_length)
                summaries = []
                
                for chunk in chunks:
                    result = model(
                        chunk,
                        max_length=request.max_length,
                        min_length=request.min_length,
                        do_sample=False
                    )
                    summaries.append(result[0]['summary_text'])
                
                # Combine summaries
                combined_summary = ' '.join(summaries)
                if len(combined_summary) > request.max_length:
                    # Summarize the combined summary
                    result = model(
                        combined_summary,
                        max_length=request.max_length,
                        min_length=request.min_length,
                        do_sample=False
                    )
                    return result[0]['summary_text']
                return combined_summary
            else:
                result = model(
                    text,
                    max_length=request.max_length,
                    min_length=request.min_length,
                    do_sample=False
                )
                return result[0]['summary_text']
                
        except Exception as e:
            raise Exception(f"Abstractive summarization failed: {str(e)}")
    
    async def _hybrid_summarize(self, text: str, request: SummarizationRequest) -> str:
        """Hybrid approach combining extractive and abstractive methods"""
        try:
            # First, extractive summarization to get key sentences
            extractive_request = SummarizationRequest(
                text=text,
                method="extractive",
                max_sentences=min(request.max_sentences * 2, len(text.split('. '))),
                max_length=request.max_length * 2,
                min_length=request.min_length,
                model=request.model
            )
            
            extractive_summary = await self._extractive_summarize(text, extractive_request)
            
            # Then, abstractive summarization of the extractive summary
            abstractive_request = SummarizationRequest(
                text=extractive_summary,
                method="abstractive",
                max_sentences=request.max_sentences,
                max_length=request.max_length,
                min_length=request.min_length,
                model=request.model
            )
            
            final_summary = await self._abstractive_summarize(extractive_summary, abstractive_request)
            return final_summary
            
        except Exception as e:
            # Fallback to extractive if hybrid fails
            return await self._extractive_summarize(text, request)
    
    def _calculate_sentence_scores(self, embeddings):
        """Calculate importance scores for sentences based on embeddings"""
        import numpy as np
        
        # Calculate similarity matrix
        similarity_matrix = np.dot(embeddings, embeddings.T)
        
        # Calculate sentence scores based on similarity to other sentences
        scores = np.sum(similarity_matrix, axis=1)
        
        # Normalize scores
        scores = scores / np.max(scores) if np.max(scores) > 0 else scores
        
        return scores
    
    async def summarize_with_openai(self, text: str, request: SummarizationRequest) -> str:
        """Summarize using OpenAI GPT models"""
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            prompt = f"""
            Please summarize the following text in {request.max_sentences} sentences or less.
            The summary should be between {request.min_length} and {request.max_length} words.
            
            Text to summarize:
            {text}
            
            Summary:
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=request.max_length * 2,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI summarization failed: {str(e)}")
    
    async def summarize_with_cohere(self, text: str, request: SummarizationRequest) -> str:
        """Summarize using Cohere models"""
        try:
            co = cohere.Client(os.getenv("COHERE_API_KEY"))
            
            response = co.summarize(
                text=text,
                length="auto",
                format="paragraph",
                model="command",
                temperature=0.3
            )
            
            return response.summary
            
        except Exception as e:
            raise Exception(f"Cohere summarization failed: {str(e)}")

# Global instance
summarizer_service = SummarizerService()
