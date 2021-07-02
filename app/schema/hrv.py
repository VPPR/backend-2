from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Hrv(BaseModel):
    id: Any
    start_time: datetime
    end_time: datetime
    sd1: float
    sd2: float
    depressed: bool
