from typing import List, Optional, Union

from fastapi.exceptions import HTTPException

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schema.user import User as UserSchema
from app.schema.user import UserCreate, UserSignUp, UserUpdate, UserUpdateSelf


class CRUDUser(
    CRUDBase[
        User,
        Union[UserCreate, UserSignUp],
        Union[UserUpdate, UserUpdateSelf],
        UserSchema,
    ]
):
    def authenticate(self, email: str, password: str) -> Optional[User]:
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
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    def create(self, user: Union[UserCreate, UserSignUp]) -> User:
        user.password = get_password_hash(user.password)
        return super().create(user)

    def update(self, model: User, obj: Union[UserUpdateSelf, UserUpdate]):
        if obj.password is not None:
            obj.password = get_password_hash(obj.password)
        return super().update(model, obj)

    def get_all_unapproved(self, skip: int, limit: int) -> List[UserSchema]:
        return list(User.object(id=id, is_approved=False).skip(skip).limit(limit))


user = CRUDUser(User)
