from sqlalchemy import ForeignKey, Enum, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from enums import Genre, AgeRating


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
    age_rating: Mapped[Enum[AgeRating]]
    date: Mapped[Date]
    director: Mapped[str]
    screenwriter: Mapped[str]
    actors: Mapped[list[str]]
    annotation: Mapped[str]


class SessionsOrm(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))


class GenresOrm(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    