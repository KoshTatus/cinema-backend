from fastapi import HTTPException
from fastapi import status

class AuthErrors:
    @staticmethod
    def get_email_occupied_error() -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is occupied!")

    @staticmethod
    def get_email_not_found_error() -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email!")

    @staticmethod
    def get_password_not_found_error() -> HTTPException:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password!")