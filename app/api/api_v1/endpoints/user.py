from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.params import Body, Path

from app import crud
from app.api.deps import get_current_admin, get_current_user
from app.models.user import User
from app.schema.response import Response
from app.schema.user import User as UserSchema
from app.schema.user import UserCreate, UserUpdate, UserUpdateSelf

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_users(_: User = Depends(get_current_admin), skip: int = 0, limit: int = 100):
    return crud.user.get_all(skip, limit)


@router.post("/", response_model=UserSchema)
def create_user(
    _: User = Depends(get_current_admin), new_user: UserCreate = Body(...)
) -> User:
    user = crud.user.create(new_user)
    return user


@router.get("/self/", response_model=Response)
def get_self(user: User = Depends(get_current_user)) -> Response:
    return Response(
        message="Data retrieved successfully", detail=UserSchema.from_orm(user)
    )


@router.delete("/self/", response_model=UserSchema)
def delete_self(user: User = Depends(get_current_user)) -> User:
    return crud.user.delete(user)


@router.put("/self/", response_model=UserSchema)
def update_self(
    user: User = Depends(get_current_user), update: UserUpdateSelf = Body(...)
) -> User:
    crud.user.update(user, update)
    return user


@router.get("/{id}/", response_model=UserSchema)
def get_user_by_id(
    user: User = Depends(get_current_admin), id: str = Path(...)
) -> User:
    queried_user = crud.user.get(id)
    if queried_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist"
        )
    return queried_user


@router.put("/{id}/", response_model=UserSchema)
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
    return queried_user


@router.delete("/{id}/", response_model=UserSchema)
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
