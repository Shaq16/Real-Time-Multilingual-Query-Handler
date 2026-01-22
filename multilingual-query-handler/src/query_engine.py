from groq import Groq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from pymongo import MongoClient
from src.embeddings import VectorStoreManager
from src.translation import TranslationEngine
from src.config import GROQ_API_KEY, MONGODB_URI, LLM_MODEL

class QueryEngine:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.vector_manager = VectorStoreManager()
        self.translator = TranslationEngine()
        self.memory = self._setup_memory()
        
        # Prompt template is now handled dynamically in process_query
        self.system_instruction = "Always answer in English."
    
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
        # Prepare messages for the LLM
        # System message defines the behavior and provides context
        system_content = f"""You are a helpful customer support assistant.
        Use the following context to answer the user's question.
        
        CONTEXT:
        {context}
        
        CRITICAL INSTRUCTION: You must ALWAYS answer in English. Do not use any other language. 
        Even if the context is in Spanish, French, or another language, translate the relevant information and answer ONLY in English.
        If you don't know the answer based on the context, say "I don't have information about that in my knowledge base" in English.
        """

        response = self.client.chat.completions.create(
            model=LLM_MODEL,  # Updated to use config variable
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": english_query}
            ],
            temperature=0.3, # Lower temperature for more deterministic behavior
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