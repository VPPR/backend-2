from typing import Any, Union
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.user import User
from app.schema.token import TokenPayload
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/login/access-token'
)

pwd_context = CryptContext(schemes=['bcrypt'])


def create_access_token(subject: Union[str, Any]):
    expire = datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRY)
    to_encode = {'exp': expire, 'subject': str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
        )
    user = User.objects(id=token_data.subject).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
