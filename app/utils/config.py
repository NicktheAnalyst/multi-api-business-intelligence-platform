import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Assign variables from environment keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")