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
async def gadgetbridge(
    user: User = Depends(get_current_user), sqlite_file: UploadFile = File(...)
):

    # Check if file uploaded is of type sqlite3
    if magic.from_buffer(sqlite_file.file.read(), mime=True) != "application/x-sqlite3":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong File type. Only sqlite file is acceptable",
        )

    # Create directory gadgetbridge to prevent the main directory from being flooded with sqlite db files
    if not os.path.exists("gadgetbridge"):
        os.makedirs("gadgetbridge")

    # Create temp db file
    filename = "gadgetbridge/" + str(uuid.uuid4()) + ".db"
    sqlite_file.file.seek(0)
    try:
        with open(filename, "wb") as f:
            shutil.copyfileobj(sqlite_file.file, f)
    finally:
        sqlite_file.file.close()
    con = sqlite3.connect(filename)
    con.row_factory = sqlite3.Row
    records = []
    cur = con.cursor()
    try:
        cur.execute("SELECT TIMESTAMP,HEART_RATE FROM MI_BAND_ACTIVITY_SAMPLE")
        for record in cur:
            record = dict(record)
            gadgetbridge = Gadgetbridge(
                user=user,
                timestamp=record.get("TIMESTAMP"),
                heart_rate=record.get("HEART_RATE"),
            )
            records.append(gadgetbridge.to_mongo())
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File doesn't contain required data",
        )
    finally:
        cur.close()
        con.close()
        os.remove(filename)
    try:
        Gadgetbridge._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )
    except Exception as e:
        print({"error": str(e)})
