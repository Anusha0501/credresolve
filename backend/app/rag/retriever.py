from typing import List, Dict, Optional
from app.rag.chroma_store import chroma_store

class KnowledgeRetriever:
    """Knowledge base retriever"""
    
    def __init__(self):
        self.store = chroma_store
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant documents"""
        results = self.store.query(query, n_results=top_k)
        
        retrieved_docs = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results.get('distances') else 0
                })
        
        return retrieved_docs
    
    def format_for_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents for context"""
        if not retrieved_docs:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc['metadata'].get('source', 'Unknown')
            content = doc['content']
            context_parts.append(f"[Source: {source}]\n{content}")
        
        return "\n\n".join(context_parts)

# Global instance
knowledge_retriever = KnowledgeRetriever()
