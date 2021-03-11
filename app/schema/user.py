from typing import Any, Optional

from pydantic import BaseModel, EmailStr, validator
from bson.objectid import ObjectId

# Shared properties
class UserBase(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_admin: Optional[bool] = None

    @validator("phone")
    def phone_validator(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if v.isnumeric() and v.startswith(("6", "7", "8", "9")) and len(v) == 10:
                return v
            else:
                raise ValueError("Phone number not valid")
        return v


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    fullname: str
    password: str
    is_admin: bool
    phone: str


# Properties to receive via API on update


class UserUpdateSelf(UserBase):
    password: Optional[str]


class UserUpdate(UserUpdateSelf):
    is_active: Optional[bool]


class User(UserBase):
    id: Any
    is_active: bool

    @validator("id")
    def validate_id(cls, id):
        return str(id)

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(User):
    password: str
