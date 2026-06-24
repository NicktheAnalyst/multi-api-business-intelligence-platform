from app.database.db import SessionLocal


def test_connection():

    session = SessionLocal()

    assert session is not None

    session.close()