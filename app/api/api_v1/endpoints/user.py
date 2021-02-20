from app.core.security import get_current_user
from fastapi.param_functions import Depends
from app.models.user import User
from fastapi import APIRouter
from app.schema.user import User as UserSchema

router = APIRouter()


@router.get("/self", response_model=UserSchema)
def get_self(user: User = Depends(get_current_user)) -> User:
    return user
