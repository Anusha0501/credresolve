import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os
from app.config import config

class ChromaStore:
    """ChromaDB vector store for RAG"""
    
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or config.CHROMA_PERSIST_DIR
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the collection"""
        try:
            self.collection = self.client.get_collection(name="debt_collection_kb")
        except:
            self.collection = self.client.create_collection(
                name="debt_collection_kb",
                metadata={"description": "Debt collection knowledge base"}
            )
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents to the collection"""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 3) -> Dict:
        """Query the collection"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents from the collection"""
        results = self.collection.get()
        documents = []
        
        for i in range(len(results['ids'])):
            documents.append({
                'id': results['ids'][i],
                'document': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        return documents

# Global instance
chroma_store = ChromaStore()
