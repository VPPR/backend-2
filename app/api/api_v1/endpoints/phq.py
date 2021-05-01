from fastapi import APIRouter, Depends
from fastapi.param_functions import Body

from app.api.deps import get_current_user
from app.models.phq import Phq

from .utils.phqutil import add_answers_to_db, all_questions, three_questions

router = APIRouter()


@router.get("/phq9")
def phq9_questions(user=Depends(get_current_user)):
    records = Phq.objects(user=user).all()
    # if no record exists, send all 9 questions
    # otherwise send 3 questions
    if not records:
        return all_questions()
    else:
        return three_questions(user)


@router.post("/phq9")
def phq9_score(user=Depends(get_current_user), body: dict = Body(...)):
    add_answers_to_db
