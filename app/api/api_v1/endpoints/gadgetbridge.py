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

router = APIRouter()


@router.post("/")
async def gb_to_mongo(
    user: User = Depends(get_current_user), sqlite_file: UploadFile = File(...)
):
    filename = str(uuid.uuid4()) + ".db"
    try:
        with open(filename, "wb") as f:
            shutil.copyfileobj(sqlite_file.file, f)
    finally:
        sqlite_file.file.close()
    if magic.from_file(filename, mime=True) != "application/x-sqlite3":
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong File type. Only sqlite file is acceptable",
        )
    con = sqlite3.connect(filename)
    # con.cursor().executescript(sqlite_file.decode("utf-8"))
    con.row_factory = sqlite3.Row

    cur = con.execute("SELECT TIMESTAMP,HEART_RATE FROM MI_BAND_ACTIVITY_SAMPLE")
    records = []
    for record in cur:
        record = dict(record)
        gadgetbridge = Gadgetbridge(
            user=user,
            timestamp=record.get("TIMESTAMP"),
            heart_rate=record.get("HEART_RATE"),
        )
        records.append(gadgetbridge.to_mongo())
    try:
        Gadgetbridge._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )
    except Exception as e:
        print({"error": str(e)})
    os.remove(filename)
