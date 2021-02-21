from typing import Any

from pydantic.main import BaseModel


class Response(BaseModel):
    message: str
    detail: Any = None
