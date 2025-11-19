import logging
from typing import Optional
import requests
from requests.exceptions import RequestException

from config import Config

logger = logging.getLogger(__name__)

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    def __init__(self, latitude: float = Config.WEATHER_LATITUDE, longitude: float = Config.WEATHER_LONGITUDE, timezone: str = Config.WEATHER_TIMEZONE):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
    def get_current_weather(self) -> Optional[str]:
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "is_day",
                "precipitation",
                "rain",
                "wind_speed_10m",
                "wind_direction_10m"
            ],
            "timezone": self.timezone,
            "forecast_days": 1
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            logger.info("Weather data fetched successfully")
            return response.text
        except RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None

def clima() -> Optional[str]:
    service = WeatherService()
    return service.get_current_weather()

