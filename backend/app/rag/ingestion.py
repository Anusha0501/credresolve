import os
from typing import List, Dict
from app.rag.chroma_store import chroma_store
from app.rag.embeddings import gemini_embeddings

class DocumentIngestion:
    """Document ingestion pipeline"""
    
    def __init__(self, knowledge_dir: str = "./knowledge"):
        self.knowledge_dir = knowledge_dir
        self.ingested_files = set()
    
    def ingest_all(self):
        """Ingest all markdown files from knowledge directory"""
        if not os.path.exists(self.knowledge_dir):
            print(f"Knowledge directory {self.knowledge_dir} does not exist")
            return
        
        files = [f for f in os.listdir(self.knowledge_dir) if f.endswith('.md')]
        
        for filename in files:
            filepath = os.path.join(self.knowledge_dir, filename)
            self.ingest_file(filepath)
    
    def ingest_file(self, filepath: str):
        """Ingest a single file"""
        if filepath in self.ingested_files:
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        
        # Split content into chunks
        chunks = self._chunk_text(content)
        
        # Create embeddings and add to ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_{i}"
            documents.append(chunk)
            metadatas.append({
                'source': filename,
                'chunk_index': i,
                'total_chunks': len(chunks)
            })
            ids.append(doc_id)
        
        chroma_store.add_documents(documents, metadatas, ids)
        self.ingested_files.add(filepath)
        print(f"Ingested {filename} with {len(chunks)} chunks")
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            if current_size + len(word) > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

# Global instance
document_ingestion = DocumentIngestion()
