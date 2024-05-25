import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

class ChatGroqManager:
    def __init__(self, model_name):
        self.model_name = model_name
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

    def create_llm(self, temperature=0.4):
        return ChatGroq(
            temperature=temperature,
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )
