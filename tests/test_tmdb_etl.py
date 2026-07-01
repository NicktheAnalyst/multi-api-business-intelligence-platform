from app.etl.tmdb_etl import transform_movies

def test_transform_movie():
    sample = {
        "results": [
            {
                "id": 1,
                "title": "Test Movie",
                "original_language": "en",
                "popularity": 100,
                "vote_average": 8,
                "vote_count": 500,
                "genre_ids": [28, 12],
                "adult": False,
                "release_date": "2025-01-01",
                "overview": "Testing"
            }
        ]
    }

    movies = transform_movies(sample)

    assert len(movies) == 1
    assert movies[0]["title"] == "Test Movie"
    assert movies[0]["rating"] == 8
    assert movies[0]["genre_ids"] == "28,12"  # Verifies your string joining logic works!