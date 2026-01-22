from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

class TranslationEngine:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
    
    def translate_to_english(self, text: str, source_language: str = "auto") -> str:
        """Translate text to English"""
        prompt = f"""Translate the following text to English. 
        Only return the translation, nothing else.
        
        Text: {text}"""
        
        response = self.client.chat.completions.create(
            model=LLM_MODEL,  # Updated to use config variable
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        prompt = f"""Detect the language of this text and return only the language name.
        
        Text: {text}"""
        
        response = self.client.chat.completions.create(
            model=LLM_MODEL,  # Updated to use config variable
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=50
        )
        
        return response.choices[0].message.content.strip()