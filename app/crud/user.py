from typing import Optional
from fastapi.exceptions import HTTPException

from app.models.user import User
from app.schema.user import UserCreate
from app.core.security import get_password_hash, verify_password


def authenticate(email: str, password: str) -> Optional[User]:
    try:
        user = User.objects(email=email).first()
        if user:
            if not verify_password(password, user.password):
                raise HTTPException(status_code=401,detail="Incorrect Password")
            if not user.is_active:
                raise HTTPException(status_code=409, detail="User Inactive")
            return user
        raise HTTPException(status_code=404, detail="User doesnt exist")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)


def signup(user: UserCreate) -> User:
    password = get_password_hash(user.password)
    db_user = User(
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        is_admin=user.is_admin,
        password=password,
        is_active=True if not user.is_admin else False
    )
    db_user.save()
    return db_user
