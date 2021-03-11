from app.models.user import User
from mongoengine.errors import NotUniqueError
from app.core.config import settings
from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.token import Token
from app import crud
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.schema.user import UserCreate, User as UserSchema

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = crud.user.authenticate(form_data.username, form_data.password)
    access_token_expires = datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRY)
    return Token(
        access_token=create_access_token(user.id, access_token_expires),
        token_type="Bearer",
        expiry=access_token_expires,
    )


@router.post("/signup", response_model=UserSchema)
def user_signup(user: UserCreate = Body(...)) -> User:
    try:
        db_user = crud.user.create(user)
        return db_user
    except NotUniqueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )


@router.get("/test", response_model=UserSchema)
def test(user=Depends(get_current_user)):
    return user
