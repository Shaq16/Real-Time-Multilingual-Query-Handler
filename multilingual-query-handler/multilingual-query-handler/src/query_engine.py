from groq import Groq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from pymongo import MongoClient
from embeddings import VectorStoreManager
from translation import TranslationEngine
from src.config import GROQ_API_KEY, MONGODB_URI, LLM_MODEL

class QueryEngine:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.vector_manager = VectorStoreManager()
        self.translator = TranslationEngine()
        self.memory = self._setup_memory()
        
        self.prompt_template = ChatPromptTemplate.from_template(
            """You are a helpful customer support assistant. 
            Use the following context to answer the user's question.
            If you don't know the answer, say so politely.
            
            Context: {context}
            
            Question: {question}
            
            Answer:"""
        )
    
    def _setup_memory(self):
        """Setup MongoDB-based conversation memory"""
        # Fallback if MongoDB is not available or configured, though logic suggests it's expected.
        # In a real scenario, you might want error handling here if URI is invalid.
        mongo_client = MongoClient(MONGODB_URI)
        memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        return memory
    
    def process_query(self, user_query: str, language: str = None) -> dict:
        """Process multilingual query and return response"""
        # Detect language if not provided
        if not language or language == "auto":
            detected_lang = self.translator.detect_language(user_query)
        else:
            detected_lang = language
        
        # Translate to English if needed
        if detected_lang.lower() != "english":
            english_query = self.translator.translate_to_english(user_query)
        else:
            english_query = user_query
        
        # Retrieve relevant documents
        relevant_docs = self.vector_manager.similarity_search(english_query, k=5)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate response
        prompt = self.prompt_template.format(
            context=context,
            question=english_query
        )
        
        response = self.client.chat.completions.create(
            model=LLM_MODEL,  # Updated to use config variable
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content
        
        return {
            "original_query": user_query,
            "detected_language": detected_lang,
            "translated_query": english_query,
            "answer": answer,
            "sources": [doc.metadata for doc in relevant_docs]
        }