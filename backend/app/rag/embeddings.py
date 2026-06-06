import google.generativeai as genai
from typing import List
from app.config import config

class GeminiEmbeddings:
    """Gemini embeddings for document processing"""
    
    def __init__(self):
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = "models/embedding-001"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a query"""
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

# Global instance
gemini_embeddings = GeminiEmbeddings()
