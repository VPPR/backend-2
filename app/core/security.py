from typing import Any, Union
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

pwd_context = CryptContext(schemes=["bcrypt"])


def create_access_token(subject: Union[str, Any], exp: datetime):
    to_encode = {"exp": exp, "subject": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
