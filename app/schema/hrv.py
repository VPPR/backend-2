from datetime import datetime

from pydantic import BaseModel


class Hrv(BaseModel):
    start_time: datetime
    end_time: datetime
    sd1: float
    sd2: float
    depressed: bool
