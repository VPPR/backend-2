from app.schema.user import User
from typing import Any, Type

from pydantic.main import BaseModel


class Response(BaseModel):
    message: str
    detail: Any = None
