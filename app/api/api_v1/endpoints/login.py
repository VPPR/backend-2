from app.core.config import settings
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.token import Token
from app.crud.user import authenticate, signup
from app.core.security import create_access_token, get_current_user
from app.schema.user import UserCreate, User as UserSchema
from app.models.user import User
from pymongo.errors import DuplicateKeyError
router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token( form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(seconds=settings.TOKEN_EXPIRY)
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }

@router.post("/signup", response_model=UserSchema)
def user_signup(user: UserCreate=Body(...)) -> UserSchema:
    try:
        db_user = signup(user)
        return db_user
    except DuplicateKeyError as inst:
        raise HTTPException(400,inst.details)
        
@router.get("/test", response_model= UserSchema)
def test(user = Depends(get_current_user)):
    return user