import os
import shutil
import sqlite3
import uuid

import magic
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from mongoengine.errors import BulkWriteError

from app.api.deps import get_current_user
from app.models.gadgetbridge import Gadgetbridge
from app.models.user import User
from app.api.api_v1.endpoints.utils import ziputils

router = APIRouter()


@router.post("/")
async def gadgetbridge(
    user: User = Depends(get_current_user), sqlite_file: UploadFile = File(...)
):
    return await ziputils.gadgetbridge(sqlite_file, user)
