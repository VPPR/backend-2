from app.models.gadgetbridge import Gadgetbridge
import os
import shutil
import uuid
import sqlite3
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from fastapi import status
import magic
import pandas
from pymongo.errors import BulkWriteError

from app.models.user import User
from app.models.zip import Activity, ActivityStage, HeartrateAuto, Sleep, Sport


async def activity(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        activity = Activity(
            date=record.get("date"),
            steps=record.get("steps"),
            distance=record.get("distance"),
            run_distance=record.get("runDistance"),
            calories=record.get("calories"),
            user=user,
        )
        records.append(activity.to_mongo())
    try:
        Activity._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )

    except Exception as e:
        print({"error": str(e)})


async def sleep(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        sleep = Sleep(
            date=record.get("date"),
            deep_sleep_time=record.get("deepSleepTime"),
            shallow_sleep_time=record.get("shallowSleepTime"),
            wake_time=record.get("wakeTime"),
            sleep_start_time=record.get("start"),
            sleep_stop_time=record.get("stop"),
            user=user,
        )
        records.append(sleep.to_mongo())
    try:
        Sleep._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )

    except Exception as e:
        print({"error": str(e)})


async def heartrate_auto(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        heartrate_auto = HeartrateAuto(
            date=record.get("date"),
            time=record.get("time"),
            heart_rate=record.get("heartRate"),
            user=user,
        )
        records.append(heartrate_auto.to_mongo())
    try:
        HeartrateAuto._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )

    except Exception as e:
        print({"error": str(e)})


async def sport(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        sport = Sport(
            sport_type=record.get("type"),
            start_time=record.get("startTime"),
            sport_time=record.get("sportTime"),
            distance=record.get("distance"),
            max_pace=record.get("maxPace"),
            min_pace=record.get("minPace"),
            avg_pace=record.get("avgPace"),
            calories=record.get("calories"),
            user=user,
        )
        records.append(sport.to_mongo())
    try:
        Sport._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )

    except Exception as e:
        print({"error": str(e)})


async def activity_stage(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        activity_stage = ActivityStage(
            date=record.get("date"),
            activity_start_time=record.get("start"),
            activity_stop_time=record.get("stop"),
            distance=record.get("distance"),
            calories=record.get("calories"),
            steps=record.get("steps"),
            user=user,
        )
        records.append(activity_stage.to_mongo())
    try:
        ActivityStage._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )

    except Exception as e:
        print({"error": str(e)})


async def gadgetbridge(sqlite_file: UploadFile, user: User):

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
