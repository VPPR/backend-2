from fastapi import APIRouter, Depends

from app.models.phq import Phq
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/phq9")
def phq9_questions(user=Depends(get_current_user)):
    pass

@router.post("/phq9")
def phq9_score():
    pass
