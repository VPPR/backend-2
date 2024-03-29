from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine.errors import NotUniqueError

from app import crud
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schema.token import Token
from app.schema.user import User as UserSchema
from app.schema.user import UserSignUp

from .utils.userutils import authenticate

router = APIRouter()


@router.post("/login/access-token/", response_model=Token)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = authenticate(form_data.username, form_data.password)
    access_token_expires = datetime.now(tz=timezone.utc) + timedelta(
        seconds=settings.TOKEN_EXPIRY
    )
    return Token(
        access_token=create_access_token(user.id, access_token_expires),
        token_type="Bearer",
        expiry=access_token_expires,
    )


@router.post("/signup/", response_model=UserSchema)
def user_signup(user: UserSignUp = Body(...)) -> User:
    try:
        db_user = crud.user.create(user)
        return db_user
    except NotUniqueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
