from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from mongoengine.errors import ValidationError

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.admin_approval import Approval
from app.models.user import User
from app.schema.user import UserCreate, UserUpdate, UserUpdateSelf


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def authenticate(self, email: str, password: str) -> Optional[User]:
        print(email)
        try:
            user = User.objects(email=email).first()
            if user:
                if not verify_password(password, user.password):
                    raise HTTPException(status_code=401, detail="Incorrect Password")
                if not user.is_active:
                    raise HTTPException(status_code=403, detail="User Inactive")
                return user
            raise HTTPException(status_code=404, detail="User doesnt exist")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    def create(self, user: UserCreate) -> User:
        password = get_password_hash(user.password)
        try:
            db_user = User(
                fullname=user.fullname,
                email=user.email,
                phone=user.phone,
                is_admin=user.is_admin,
                password=password,
                is_active=True if not user.is_admin else False,
            )
            db_user.save()
            if user.is_admin:
                Approval(user=db_user).save()

        except ValidationError as e:
            print(e.__dict__)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fuck you"
            )

        return db_user

    def update_self(self, model: User, obj: UserUpdateSelf):
        if obj.password is not None:
            obj.password = get_password_hash(obj.password)
        return super().update(model, obj)


user = CRUDUser(User)
