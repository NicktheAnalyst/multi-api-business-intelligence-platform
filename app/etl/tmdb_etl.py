import requests
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from app.database.db import SessionLocal
from app.database.models import Movie
from app.utils.config import TMDB_API_TOKEN
from app.utils.logger import logger
from app.database.db import engine, Base

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_TOKEN}",
    "accept": "application/json"
}


def extract_movies(page=1):
    url = "https://api.themoviedb.org/3/trending/movie/day"
    params = {
        "page": page
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def transform_movies(data):
    movies = []
    for movie in data["results"]:
        # Safety check and conversion from string to a Python date object
        raw_date = movie.get("release_date")
        release_date_obj = None
        if raw_date:
            try:
                release_date_obj = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except ValueError:
                release_date_obj = None

        movies.append({
            "movie_id": movie["id"],
            "title": movie["title"],
            "original_language": movie["original_language"],
            "popularity": movie["popularity"],
            "rating": movie["vote_average"],
            "vote_count": movie["vote_count"],
            "genre_ids": ",".join(map(str, movie["genre_ids"])),
            "adult": movie["adult"],
            "release_date": release_date_obj,  # Injected Python date object
            "overview": movie["overview"],
            "collected_at": datetime.now(timezone.utc)
        })
    return movies


def validate_movie(movie):
    if not movie["title"]:
        return False
    if movie["rating"] is None:
        return False
    if movie["vote_count"] < 10:
        return False
    return True


def load_movies(session, movies):
    inserted = 0
    for movie in movies:
        if not validate_movie(movie):
            continue
        try:
            with session.begin_nested():
                session.add(Movie(**movie))
            inserted += 1
        except IntegrityError:
            continue

    session.commit()
    return inserted


def run_tmdb_etl():
    logger.info("TMDB ETL started")
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    total = 0

    try:
        for page in range(1, 4):
            raw = extract_movies(page)
            movies = transform_movies(raw)
            total += load_movies(session, movies)

        logger.info(f"Loaded {total} movies")

    except Exception:
        logger.exception("TMDB ETL failed.")
        session.rollback()
    finally:
        session.close()
        logger.info("TMDB ETL finished.")


if __name__ == "__main__":
    run_tmdb_etl()