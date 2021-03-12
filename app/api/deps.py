from mongoengine.errors import ValidationError
from app.schema.token import TokenPayload
from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_scheme
from jose import jwt
from app.core.config import settings
from app import crud
from app.schema.user import User


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
            detail="Could not validate credentials",
        )
    user = crud.user.get(id=token_data.subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=409, detail="User Inactive")
    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.is_admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized Resource. Access is forbidden",
    )
