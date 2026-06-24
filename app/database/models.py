from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.db import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(
        Integer,
        primary_key=True
    )
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    condition = Column(String)
    timestamp = Column(DateTime)


class Currency(Base):
    __tablename__ = "currency"

    id = Column(
        Integer,
        primary_key=True
    )
    base_currency = Column(String)
    target_currency = Column(String)
    exchange_rate = Column(Float)
    timestamp = Column(DateTime)


class News(Base):

    __tablename__ = "news"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(String)

    author = Column(String)

    source = Column(String)

    category = Column(String)

    published_at = Column(DateTime)   


class Movie(Base):

    __tablename__ = "movies"

    id = Column(
        Integer,
        primary_key=True
    )

    movie_id = Column(Integer)

    title = Column(String)

    popularity = Column(Float)

    rating = Column(Float)

    release_date = Column(String)


class Country(Base):

    __tablename__ = "countries"

    id = Column(
        Integer,
        primary_key=True
    )

    country = Column(String)

    capital = Column(String)

    population = Column(Integer)

    currency = Column(String)

    region = Column(String)