from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expiry: datetime
    


class TokenPayload(BaseModel):
    subject: Optional[str] = None
