from typing import Any, Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @validator("phone")
    def phone_validator(cls, phone: Optional[str]) -> Optional[str]:
        if phone is None or (
            phone is not None
            and phone.isnumeric()
            and phone.startswith(("6", "7", "8", "9"))
            and len(phone) == 10
        ):
            return phone
        else:
            raise ValueError("Phone number not valid")


class UserSignUp(UserBase):
    fullname: str
    email: EmailStr
    phone: str
    password: str


class UserCreate(UserSignUp):
    is_active: bool
    is_admin: bool


# Properties to receive via API on update


class UserUpdateSelf(UserBase):
    password: Optional[str]


class UserUpdate(UserUpdateSelf):
    is_active: Optional[bool]
    is_admin: Optional[bool]


class User(UserBase):
    id: Any
    fullname: str
    email: EmailStr
    phone: str
    is_active: bool
    is_admin: bool

    @validator("id")
    def validate_id(cls, id):
        return str(id)

    class Config:
        orm_mode = True
