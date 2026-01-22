import re
from typing import List
from langchain.schema import Document

class DataPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """Preprocess all documents"""
        cleaned_docs = []
        
        for doc in documents:
            cleaned_content = self.clean_text(doc.page_content)
            
            if cleaned_content:  # Only keep non-empty documents
                doc.page_content = cleaned_content
                cleaned_docs.append(doc)
        
        return cleaned_docs