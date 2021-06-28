from fastapi import APIRouter, Depends, File, UploadFile

from app.api.api_v1.endpoints.utils import ziputils
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", status_code=200)
async def gadgetbridge(
    user: User = Depends(get_current_user), sqlite_file: UploadFile = File(...)
):
    return await ziputils.gadgetbridge(sqlite_file, user)
