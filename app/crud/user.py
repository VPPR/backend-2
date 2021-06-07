from typing import List, Union
from app.core.security import get_password_hash
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
    def create(self, user: Union[UserCreate, UserSignUp]) -> User:
        user.password = get_password_hash(user.password)
        return super().create(user)

    def update(self, model: User, obj: Union[UserUpdateSelf, UserUpdate]):
        if obj.password is not None:
            obj.password = get_password_hash(obj.password)
        return super().update(model, obj)

    def get_by_email(self, email: str):
        user = User.objects(email=email).first()
        return user

    # def get_all_unapproved(self, skip: int, limit: int) -> List[UserSchema]:
    #     return list(User.object(id=id, is_approved=False).skip(skip).limit(limit))


user = CRUDUser(User)
