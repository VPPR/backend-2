from fastapi import APIRouter, Depends
from fastapi.param_functions import Body, 

from app.models.phq import Phq
from app.api.deps import get_current_user
from .utils.phqutil import add_answers_to_db, all_questions, three_questions

router = APIRouter()

@router.get("/phq9")
def phq9_questions(user=Depends(get_current_user)):
    records = Phq.objects(id=user)
    # if no record exists, send all 9 questions
    # otherwise send 3 questions
    if not records:
        all_questions()
    else:
        three_questions(user)

@router.post("/phq9")
def phq9_score(user=Depends(get_current_user), body: dict = Body(...)):
    add_answers_to_db
