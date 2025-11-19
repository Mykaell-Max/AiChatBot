import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN: str = os.getenv('TOKEN', '')
    GOOGLE_API_KEY: str = os.getenv('GOOGLE', '')
    BOT_PREFIX: str = '!'
    BOT_NAME: str = 'ChatBot'
    NOTIFICATION_CHANNEL_ID: Optional[int] = None
    WEATHER_LATITUDE: float = -18.9113
    WEATHER_LONGITUDE: float = -48.2622
    WEATHER_TIMEZONE: str = "America/Sao_Paulo"
    GEMINI_MODEL: str = 'gemini-1.5-flash'
    EMBED_COLOR_SUCCESS: int = 0x00FF00
    EMBED_COLOR_ERROR: int = 0xFF0000
    EMBED_COLOR_INFO: int = 0x3498db
    EMBED_COLOR_WARNING: int = 0xFFA500

    @classmethod
    def validate(cls) -> bool:
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN not set in .env")
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in .env")
        return True

Config.validate()