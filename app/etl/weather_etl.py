import requests

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.utils.config import OPENWEATHER_API_KEY

from app.utils.logger import logger

from app.database.db import SessionLocal

from app.database.models import Weather


import os
from datetime import datetime, timezone
import requests

# Assuming these are imported from your setup
# from database import SessionLocal, Weather
# from utils.logger import logger
# OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = [
    "Nairobi",
    "London",
    "New York",
    "Tokyo"
]


def validate_weather(data):
    if data["temperature"] is None:
        return False
    if data["humidity"] is None:
        return False
    return True


def extract_weather(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.exception(f"Weather extraction failed: {city}")
        return None
    

def transform_weather(data):
    if not data:
        return None

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "timestamp": datetime.now(timezone.utc)
    }


def load_weather(session, weather_data):
    weather = Weather(
        city=weather_data["city"],
        temperature=weather_data["temperature"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
        condition=weather_data["condition"],
        timestamp=weather_data["timestamp"]
    )
    session.add(weather)


def run_weather_etl():
    logger.info("Weather ETL started")
    session = SessionLocal()

    try:
        count = 0
        for city in CITIES:
            raw_data = extract_weather(city)
            transformed = transform_weather(raw_data)

            if transformed and validate_weather(transformed):
                load_weather(session, transformed)
                count += 1

        session.commit()
        logger.info(f"Inserted {count} weather records")

    except Exception:
        session.rollback()
        logger.exception("Weather ETL failed")

    finally:
        session.close()
        logger.info("Weather ETL finished")


if __name__ == "__main__":
    run_weather_etl()