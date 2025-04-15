import hashlib

from fastapi import HTTPException
from src.auth.jwt_auth.base.auth import JWTAuth
from jwt.exceptions import InvalidTokenError

def try_to_decode_token(jwt_auth: JWTAuth, token: str) -> dict | InvalidTokenError:
    try:
        payload = jwt_auth.verify_token(token)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=400,
            detail="Invalid token!"
        )

def hash_password(password: str):
    coder = hashlib.new("sha256")
    coder.update(password.encode(encoding="utf-8"))
    return coder.hexdigest()