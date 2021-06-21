from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.prediction import Prediction
from app.schema.hrv import Hrv

router = APIRouter()


@router.post("/", response_model=List[Hrv])
def hrv_predictions(user=Depends(get_current_user)):
    records = Prediction.objects(user=user).order_by("-start_time").all()
    predictions = []
    if not records:
        return []
    else:
        for i in records:
            predictions.append(
                Hrv(
                    start_time=datetime.fromtimestamp(i.start_time, tz=timezone.utc),
                    end_time=datetime.fromtimestamp(i.end_time, tz=timezone.utc),
                    sd1=i.sd1,
                    sd2=i.sd2,
                    depressed=i.depressed,
                )
            )
    return predictions