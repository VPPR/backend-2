from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body

from app.api.deps import get_current_user
from app.models.phq import AvgAndEstimatedPhqScore, Phq
from app.schema.phq import PhqScore, Question, SingleQuestionResponce

from .utils.phqutil import (
    add_answers_to_db,
    all_questions,
    fix_missing_records,
    three_questions,
    update_avg_and_estm_phq,
)

router = APIRouter()


@router.get("/", response_model=Dict[str, Question])
def phq9_questions(user=Depends(get_current_user)):
    records = Phq.objects(user=user).all()
    # if no record exists, send all 9 questions
    # otherwise send 3 questions
    if not records:
        return all_questions()
    else:
        return three_questions(user)


@router.post("/", status_code=200)
def phq9_score(
    user=Depends(get_current_user), body: Dict[int, SingleQuestionResponce] = Body(...)
):
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record and record.last_fixed.date() < datetime.now(tz=timezone.utc).date():
        fix_missing_records(user, record.last_fixed)
    add_answers_to_db(user, body)
    update_avg_and_estm_phq(user, body)


@router.get("/score", response_model=PhqScore)
def get_phq_score(user=Depends(get_current_user)):
    record = record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record:
        return PhqScore(score=record.estimated_phq, last_answered=record.last_updated)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Haven't answered any questions yet 😞",
    )
