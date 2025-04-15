from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from src.auth.jwt_auth.base.auth import JWTAuth
from src.auth.jwt_auth.base.config import JWTConfig
from src.auth.jwt_auth.utils import try_to_decode_token
from src.auth.service import AuthService
from src.auth.utils import get_users
from src.database import get_db
from src.schemas import User, UserForm, UserInfo

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_auth_service():
    return AuthService(jwt_auth=JWTAuth(config=JWTConfig()))


def get_current_auth_user_info(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
) -> UserInfo:
    cookie_header = request.headers.get("Cookie")
    if not cookie_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cookie not found"
        )

    token = None
    for chunk in cookie_header.split(";"):
        if "access_token" in chunk:
            token = chunk.split("=")[1].strip()
            break

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found in cookies"
        )

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = try_to_decode_token(auth_service.jwt_auth, token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return UserInfo(
        id=payload.get("id"),
        is_admin=payload.get("isAdmin"),
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
        user: UserForm,
        auth_service: AuthService = Depends(get_auth_service),
        db: Session = Depends(get_db)
):
    data = auth_service.register(user, db)
    return {
        "data" : {
            "token": data
        }
    }


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
        user: UserForm,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
        db: Session = Depends(get_db)
):
    data = auth_service.login(user, db)
    response.set_cookie("access_token", data)
    return {
        "data" : {
            "token": data
        }
    }


@router.get("/users")
def users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/test")
def auth_user_check(
        user: User = Depends(get_current_auth_user_info)
):
    return user
