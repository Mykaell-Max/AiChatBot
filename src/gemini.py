import logging
from typing import Optional
import google.generativeai as genai

from config import Config
from promptConfig import initial_context

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str = Config.GOOGLE_API_KEY, model_name: str = Config.GEMINI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        self._configure_api()
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=initial_context)
        logger.info(f"Gemini service started with model {self.model_name}")

    def _configure_api(self) -> None:
        genai.configure(api_key=self.api_key)

    def get_chat(self):
        return self.chat

    def send_message(self, message: str) -> Optional[str]:
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            logger.error(f"Error sending message to Gemini: {e}")
            return None

_gemini_service = GeminiService()
chat = _gemini_service.get_chat()