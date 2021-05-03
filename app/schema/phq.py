from pydantic import BaseModel


class SingleQuestionResponce(BaseModel):
    qno: int
    score: int
    version: int
