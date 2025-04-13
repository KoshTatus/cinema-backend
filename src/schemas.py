from pydantic import BaseModel, EmailStr, Field

MIN_LENGTH_PASSWORD = 8
MAX_LENGTH_PASSWORD = 20

class UserForm(BaseModel):
    email: EmailStr = Field(title="Email", default="user@example.com")
    password: str = Field(title="Password", min_length=MIN_LENGTH_PASSWORD, max_length=MAX_LENGTH_PASSWORD)


class UserCreate(BaseModel):
    email: str
    password_hash: str
