import datetime

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from src.enums import AgeRating

MIN_LENGTH_PASSWORD = 8
MAX_LENGTH_PASSWORD = 20
MIN_LENGTH_INFO = 10
MAX_LENGTH_INFO = 50

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

class User(UserCreate):
    id: int
    is_admin: bool

class Movie(BaseModel):
    id: int
    title: str
    genre: int
    age_rating: AgeRating
    director: str
    screenwriter: str
    actors: list[str]
    description: str
    trailer_url: str
    poster_url: str

class Genre(BaseModel):
    id: int
    name: str

class OrderForm(BaseModel):
    user_id: int
    movie_id: int
    info: str = Field(default="+79998887766", min_length=MIN_LENGTH_INFO, max_length=MAX_LENGTH_INFO)
    sum: int

class Order(BaseModel):
    id: int
    user_id: int
    movie_id: int
    info: str
    sum: int
    created_at: datetime.datetime

class Session(BaseModel):
    id: int
    movie_id: int
    date: datetime.datetime