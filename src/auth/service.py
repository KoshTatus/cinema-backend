from sqlalchemy.orm import Session

from src.auth.errors import AuthErrors
from src.auth.jwt_auth.base.auth import JWTAuth
from src.auth.jwt_auth.utils import hash_password
from src.auth.utils import user_exist, add_user, email_exist, password_exist
from src.crud import get_user_by_email
from src.schemas import UserForm, UserCreate


class AuthService:
    def __init__(self, jwt_auth: JWTAuth):
        self.jwt_auth = jwt_auth

    def register(self, user: UserForm, db: Session):
        if user_exist(user.email, db):
            raise AuthErrors.get_email_occupied_error()
        add_user(
            UserCreate(
                email=user.email,
                password_hash=hash_password(user.password)
            ),
            db
        )

        user = get_user_by_email(user.email, db)

        token = self.jwt_auth.generate_token(
            payload={
                "id" : user.id,
                "isAdmin" : user.is_admin,
            }
        )
        return token

    def login(self, user: UserForm, db: Session):
        if not email_exist(user.email, db):
            raise AuthErrors.get_email_not_found_error()
        if not password_exist(user.password, db):
            raise AuthErrors.get_password_not_found_error()

        user = get_user_by_email(user.email, db)

        token = self.jwt_auth.generate_token(
            payload={
                "id": user.id,
                "isAdmin": user.is_admin,
            }
        )
        return token


