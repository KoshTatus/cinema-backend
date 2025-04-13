import datetime
from typing import List

from sqlalchemy import ForeignKey, Enum, Date, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from enums import AgeRating

class Base(DeclarativeBase):
    pass

class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str]
    password_hash: Mapped[str]


class MoviesOrm(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    genre: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    age_rating: Mapped[AgeRating]
    director: Mapped[str]
    screenwriter: Mapped[str]
    actors: Mapped[list[str]] = mapped_column(JSON)
    description: Mapped[str]
    trailer_url: Mapped[str]
    poster_url: Mapped[str]


class SessionsOrm(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    date: Mapped[datetime.datetime]


class GenresOrm(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class OrdersOrm(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    info: Mapped[str]
    sum: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())