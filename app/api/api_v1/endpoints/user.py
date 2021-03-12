from app import crud
from typing import List
from bson.objectid import ObjectId
from fastapi.params import Body, Path
from pydantic.networks import EmailStr
from app.schema.response import Response
from fastapi.exceptions import HTTPException
from app.api.deps import get_current_user, get_current_admin
from fastapi.param_functions import Depends
from app.models.user import User
from fastapi import APIRouter, status
from app.schema.user import User as UserSchema, UserCreate, UserUpdate, UserUpdateSelf

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_users(_: User = Depends(get_current_admin), skip: int = 0, limit: int = 100):
    return crud.user.get_all(skip, limit)


@router.get("/self", response_model=Response)
def get_self(user: User = Depends(get_current_user)) -> Response:
    return Response(
        message="Data retrieved successfully", detail=UserSchema.from_orm(user)
    )


@router.delete("/self", response_model=UserSchema)
def delete_self(user: User = Depends(get_current_user)) -> User:
    return crud.user.delete(user)


@router.put("/self", response_model=UserSchema)
def update_self(
    user: User = Depends(get_current_user), update: UserUpdateSelf = Body(...)
) -> User:
    # update = UserUpdate(fullname=fullname, email=email, phone=phone, password=password)
    # if fullname is not None:
    #     update.fullname = fullname
    # if email is not None:
    #     update.email = email
    # if phone is not None and is_phone_valid(phone):
    #     update.phone = phone
    # if password is not None:
    #     update.password = get_password_hash(password)
    crud.user.update(user, update)
    return user


@router.get("/{id}", response_model=UserSchema)
def get_user_by_id(
    user: User = Depends(get_current_admin), id: str = Path(...)
) -> User:
    queried_user = crud.user.get(id)
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
    queried_user: User = crud.user.get(id=id)
    if queried_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist"
        )
    queried_user = crud.user.update(queried_user, update)

    # if update.fullname is not None:
    #     queried_user.fullname = update.fullname
    # if update.email is not None:
    #     queried_user.email = update.email
    # if update.phone is not None and is_phone_valid(update.phone):
    #     queried_user.phone = update.phone
    # if update.password is not None:
    #     queried_user.password = get_password_hash(update.password)
    # if update.is_admin is not None:
    #     queried_user.is_admin = update.is_admin
    # queried_user.save()
    return queried_user


@router.delete("/{id}", response_model=UserSchema)
def delete_user_by_id(
    user: User = Depends(get_current_admin), id: str = Path(...)
) -> User:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid Id")
    queried_user: User = crud.user.get(id=id)
    if queried_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist"
        )
    return crud.user.delete(queried_user)
