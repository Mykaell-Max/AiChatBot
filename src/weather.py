import requests

def clima():
    infos = {
        "latitude": -18.9113,
        "longitude": -48.2622,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1
    }

    resp = requests.get('https://api.open-meteo.com/v1/forecast', infos)

    return resp.text

