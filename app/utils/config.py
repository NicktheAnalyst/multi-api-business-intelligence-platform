from dotenv import load_dotenv
import os

load_dotenv()

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

NEWS_API_KEY = os.getenv(
    "NEWS_API_KEY"
)

TMDB_API_TOKEN = os.getenv(
    "TMDB_API_TOKEN"
)

EXCHANGE_RATE_API_KEY = os.getenv(
    "EXCHANGE_RATE_API_KEY"
)


