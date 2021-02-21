from app.utils.validators import is_phone_valid
from fastapi.params import Body
from pydantic.networks import EmailStr
from app.schema.response import Response
from fastapi.exceptions import HTTPException
from app.core.security import get_current_user, get_password_hash
from fastapi.param_functions import Depends
from app.models.user import User
from fastapi import APIRouter, status
from app.schema.user import User as UserSchema, UserUpdate

router = APIRouter()


@router.get("/self", response_model=UserSchema)
def get_self(user: User = Depends(get_current_user)) -> User:
    return user


@router.delete("/self", response_model=UserSchema)
def delete_self(user: User = Depends(get_current_user)) -> User:
    user.delete()
    return user


@router.put("/self", response_model=UserSchema)
def update_self(
    user: User = Depends(get_current_user),
    fullname: str = Body(None),
    email: EmailStr = Body(None),
    phone: str = Body(None),
    password: str = Body(None),
) -> User:
    if fullname is not None:
        user.fullname = fullname
    if email is not None:
        user.email = email
    if phone is not None and is_phone_valid(phone):
        user.phone = phone
    if password is not None:
        user.password = get_password_hash(password)
    user.save()
    return user
