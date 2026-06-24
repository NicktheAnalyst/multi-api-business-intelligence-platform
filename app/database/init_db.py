from app.database.db import engine
from app.database.db import Base

from app.database import models


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database tables created."
    )


if __name__ == "__main__":
    create_tables()