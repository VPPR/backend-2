from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.phq import AvgAndEstimatedPhqScore, Phq
from app.schema.phq import PhqScore, Question, SingleQuestionResponse

from .utils.phqutil import (
    add_answers_to_db,
    all_questions,
    fix_missing_records,
    three_questions,
    update_avg_and_estm_phq,
)

router = APIRouter()


@router.get("/", response_model=List[Question])
def phq9_questions(user=Depends(get_current_user)):
    records = Phq.objects(user=user).all()
    # if no record exists, send all 9 questions
    # otherwise send 3 questions
    if not records:
        return all_questions(user)
    else:
        return three_questions(user)


@router.post("/", status_code=200)
def phq9_score(
    user=Depends(get_current_user), body: List[SingleQuestionResponse] = Body(...)
):
    if body and (len(body) == 9 or len(body) == 3):
        record = (
            AvgAndEstimatedPhqScore.objects(user=user, fixed=False)
            .order_by("+date")
            .first()
        )
        if record and record.date < datetime.now(tz=timezone.utc).date():
            print("fexing shit")
            fix_missing_records(user, record.date)
        add_answers_to_db(user, body)
        update_avg_and_estm_phq(user, body)
    else:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable entity"
        )


@router.get("/score", response_model=PhqScore)
def get_phq_score(user=Depends(get_current_user)):
    record = record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record:
        return PhqScore(score=record.estimated_phq, last_answered=record.last_updated)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Haven't answered any questions yet 😞",
    )
