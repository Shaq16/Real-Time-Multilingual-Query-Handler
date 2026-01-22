from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
from langchain.schema import Document
from src.config import EMBEDDING_MODEL, COLLECTION_NAME

class VectorStoreManager:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        self.persist_directory = persist_directory
        self.vectorstore = None
    
    def create_vectorstore(self, documents: List[Document]):
        """Create vector store from documents"""
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=self.persist_directory
        )
        return self.vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=COLLECTION_NAME
        )
        return self.vectorstore
    
    def similarity_search(self, query: str, k: int = 5):
        """Search for similar documents"""
        if not self.vectorstore:
            self.load_vectorstore()
        
        results = self.vectorstore.similarity_search(query, k=k)
        return results