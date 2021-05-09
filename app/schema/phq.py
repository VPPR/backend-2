from datetime import datetime

from pydantic import BaseModel, validator


class Question(BaseModel):
    qno: int
    question: str
    version: int
    average_score: int


class SingleQuestionResponse(BaseModel):
    qno: int
    score: int
    version: int

    @validator("qno")
    def validate_qno_value(qno: int):
        if 1 <= qno <= 9:
            return qno
        else:
            raise ValueError("qno can be integer value from 1 to 9")

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


class SingleQuestionResponseFloat(BaseModel):
    qno: int
    score: float
    version: float

    @validator("qno")
    def validate_qno_value(qno: int):
        if 1 <= qno <= 9:
            return qno
        else:
            raise ValueError("qno can be integer value from 1 to 9")

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
