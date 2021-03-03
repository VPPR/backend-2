from typing import Optional
from fastapi.exceptions import HTTPException
from mongoengine.errors import ValidationError
from fastapi import status
from app.models.user import User
from app.models.admin_approval import Approval
from app.schema.user import UserCreate
from app.core.security import get_password_hash, verify_password


def authenticate(email: str, password: str) -> Optional[User]:
    try:
        user = User.objects(email=email).first()
        if user:
            if not verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="Incorrect Password")
            if not user.is_active:
                raise HTTPException(status_code=409, detail="User Inactive")
            return user
        raise HTTPException(status_code=404, detail="User doesnt exist")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)


def signup(user: UserCreate) -> User:
    password = get_password_hash(user.password)
    try:
        db_user = User(
            fullname=user.fullname,
            email=user.email,
            phone=user.phone,
            is_admin=user.is_admin,
            password=password,
        )
        if user.is_admin:
            db_user.is_active = False
            db_user.save()
            Approval(user=db_user).save()
        else:
            db_user.is_active = True

        db_user.save()
    except ValidationError as e:
        print(e.__dict__)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fuck you"
        )

    return db_user
