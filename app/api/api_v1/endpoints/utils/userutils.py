from typing import Optional

from fastapi.exceptions import HTTPException

from app import crud
from app.core.security import verify_password
from app.models.user import User


def authenticate(email: str, password: str) -> Optional[User]:
    try:
        user = crud.user.get_by_email(email)
        if user:
            if not verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="Incorrect Password")
            if not user.is_active:
                raise HTTPException(status_code=403, detail="User Inactive")
            return user
        raise HTTPException(status_code=404, detail="User doesnt exist")
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
