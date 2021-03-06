from datetime import datetime

from pydantic import BaseModel, validator


class Question(BaseModel):
    question: str
    version: int


class SingleQuestionResponce(BaseModel):
    score: int
    version: int

    @validator("score")
    def validate_score_value(score: int):
        if 0 <= score <= 3:
            return score
        else:
            raise ValueError("score can be integer value from 0 to 3")

    @validator("version")
    def validate_version_value(version: int):
        if 1 <= version <= 2:
            return version
        else:
            raise ValueError("version can be either 0 or 1")


class SingleQuestionResponceFloat(BaseModel):
    score: float
    version: float

    @validator("score")
    def validate_score_value(score: int):
        if 0 <= score <= 3:
            return score
        else:
            raise ValueError("score can be integer value from 0 to 3")

    @validator("version")
    def validate_version_value(version: int):
        if 1 <= version <= 2:
            return version
        else:
            raise ValueError("version can be either 0 or 1")


class PhqScore(BaseModel):
    score: float
    last_answered: datetime
