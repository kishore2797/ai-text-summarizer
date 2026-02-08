import re
import nltk
from typing import List
import PyPDF2
from docx import Document
import io

class TextProcessor:
    def __init__(self):
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\(\)]', '', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([\.!\?,;:])', r'\1', text)
        
        # Ensure text starts with capital letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text.strip()
    
    def chunk_text(self, text: str, max_length: int = 1024) -> List[str]:
        """Split text into chunks of specified maximum length"""
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) <= max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return self.preprocess_text(text)
            
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def extract_text_from_docx(self, docx_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(docx_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self.preprocess_text(text)
            
        except Exception as e:
            raise Exception(f"DOCX processing failed: {str(e)}")
    
    def extract_text_from_txt(self, txt_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            text = txt_content.decode('utf-8')
            return self.preprocess_text(text)
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                text = txt_content.decode('latin-1')
                return self.preprocess_text(text)
            except Exception as e:
                raise Exception(f"Text file processing failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Text file processing failed: {str(e)}")
    
    def get_text_statistics(self, text: str) -> dict:
        """Get basic statistics about the text"""
        words = text.split()
        sentences = nltk.sent_tokenize(text)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "character_count": len(text),
            "character_count_no_spaces": len(text.replace(" ", "")),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "avg_chars_per_word": sum(len(word) for word in words) / len(words) if words else 0
        }
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common words"""
        # This is a simplified version - in production, use a proper language detection library
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        spanish_words = ['el', 'la', 'y', 'o', 'pero', 'en', 'a', 'para', 'de', 'con', 'por']
        french_words = ['le', 'la', 'et', 'ou', 'mais', 'dans', 'à', 'pour', 'de', 'avec', 'par']
        
        text_lower = text.lower()
        words = set(text_lower.split())
        
        english_count = len(words.intersection(english_words))
        spanish_count = len(words.intersection(spanish_words))
        french_count = len(words.intersection(french_words))
        
        if english_count > spanish_count and english_count > french_count:
            return "english"
        elif spanish_count > english_count and spanish_count > french_count:
            return "spanish"
        elif french_count > english_count and french_count > spanish_count:
            return "french"
        else:
            return "unknown"
