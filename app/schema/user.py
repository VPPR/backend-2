from typing import Optional

from pydantic import BaseModel, EmailStr, validator


# Shared properties
class UserBase(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_admin: bool = False

    @validator('phone')
    def phone_validator(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if v.isnumeric() and v.startswith(('6', '7', '8', '9')) and len(v) == 10:
                return v
            else:
                raise ValueError('Phone number not valid')
        return v


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    fullname: str
    password: str
    is_admin: bool
    phone: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    _id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
