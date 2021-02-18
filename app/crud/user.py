from typing import Optional
from fastapi.exceptions import HTTPException
from app.models.user import User
from app.schema.user import UserCreate, UserInDB,User as  UserSchema
from app.core.security import get_password_hash, verify_password
def authenticate(email:str, password:str) -> Optional[User]:
    try:
        user = User.objects(email=email).first()
        return user if verify_password(password,user.password) else None
        
    except Exception as e:
        raise HTTPException(status_code=401,detail=e.detail)

def signup(user: UserCreate) -> User:
    password=get_password_hash(user.password)
    db_user=User(user.fullname,user.email,user.phone,user.is_admin,password)
    db_user.save()
    return db_user
