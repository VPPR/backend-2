from bson.objectid import ObjectId
from app.utils.validators import is_phone_valid
from fastapi.params import Body, Path
from pydantic.networks import EmailStr
from app.schema.response import Response
from fastapi.exceptions import HTTPException
from app.core.security import get_current_admin, get_current_user, get_password_hash
from fastapi.param_functions import Depends
from app.models.user import User
from fastapi import APIRouter, status
from app.schema.user import User as UserSchema, UserUpdate

router = APIRouter()


@router.get("/self", response_model=Response)
def get_self(user: User = Depends(get_current_user)) -> Response:
    return Response(message="Data retrieved successfully", detail=UserSchema.from_orm(user))


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


@router.get("/{id}", response_model=UserSchema)
def get_user_by_id(
    user: User = Depends(get_current_admin), id: str = Path(...)
) -> User:
    queried_user = User.objects(id=id).first()
    if queried_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist"
        )
    return queried_user


@router.put("/{id}", response_model=UserSchema)
def update_user_by_id(
    user: User = Depends(get_current_admin),
    id: str = Path(...),
    update: UserUpdate = Body(...),
) -> User:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid Id")
    queried_user: User = User.objects(id=id).first()
    if queried_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist"
        )
    if update.fullname is not None:
        queried_user.fullname = update.fullname
    if update.email is not None:
        queried_user.email = update.email
    if update.phone is not None and is_phone_valid(update.phone):
        queried_user.phone = update.phone
    if update.password is not None:
        queried_user.password = get_password_hash(update.password)
    if update.is_admin is not None:
        queried_user.is_admin = update.is_admin
    queried_user.save()
    return queried_user


@router.delete("/{id}", response_model=UserSchema)
def delete_user_by_id(
    user: User = Depends(get_current_admin), id: str = Path(...)
) -> User:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid Id")
    queried_user = User.objects(id=id).first()
    queried_user.delete()
    return queried_user
