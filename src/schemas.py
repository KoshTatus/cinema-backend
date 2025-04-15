import datetime

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, PositiveInt

from src.enums import AgeRating

MIN_LENGTH_PASSWORD = 8
MAX_LENGTH_PASSWORD = 20
MIN_LENGTH_INFO = 10
MAX_LENGTH_INFO = 50


class Movie(BaseModel):
    id: int
    title: str
    director: str
    screenwriter: str
    actors: list[str]
    description: str
    trailer_url: str
    poster_url: str
    age_rating: AgeRating
    duration: int


class Hall(BaseModel):
    id: int
    name: str
    total_seats: int


class Genre(BaseModel):
    id: int
    name: str


class Session(BaseModel):
    id: int
    movie_id: int
    hall_id: int
    start_time: datetime.datetime


class SessionDetailed(BaseModel):
    id: int
    movie: Movie
    hall: Hall
    start_time: datetime.datetime


class Seat(BaseModel):
    id: int
    hall_id: int
    row_number: int
    seat_number: int
    price: int
    is_available: bool


class OrderCreate(BaseModel):
    seats_ids: list[int]
    user_id: int
    session_id: int
    total_price: int
    info: str = Field(min_length=MIN_LENGTH_INFO, max_length=MAX_LENGTH_INFO)


class Order(BaseModel):
    id: int
    user_id: int
    session_id: int
    total_price: int
    info: str
    created_at: datetime.datetime


class OrderDetailed(Order):
    seats: list[Seat]

class SessionFilters(BaseModel):
    title: str = Field(
        description="Название фильма"
    )
    genre: str = Field(
        description="Название жанра"
    )
    age: str = Field(
        description="Возрастной рейтинг"
    )
    start_date: datetime.datetime = Field(
        default=datetime.datetime.now(),
        description="Начало даты поиска"
    )
    end_date: datetime.datetime = Field(
        default=datetime.datetime.now() + datetime.timedelta(days=7),
        description="Конец даты поиска"
    )


class UserForm(BaseModel):
    email: EmailStr = Field(title="Email", default="user@example.com")
    password: str = Field(
        title="Password",
        min_length=MIN_LENGTH_PASSWORD,
        max_length=MAX_LENGTH_PASSWORD,
        default="12345678"
    )


class UserCreate(BaseModel):
    email: str
    password_hash: str

class UserInfo(BaseModel):
    id: int
    is_admin: bool

class User(UserCreate, UserInfo):
    created_at: datetime.datetime


class UserWithOrders(BaseModel):
    user: User
    orders: list[OrderDetailed]
