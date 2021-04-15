import io
import pandas
from fastapi.datastructures import UploadFile
from pymongo.errors import BulkWriteError
from app.models.user import User
from app.models.zip import Activity, ActivityStage, HeartrateAuto, Sleep, Sport
from app.schema.user import User as UserSchema


async def parse_data(file: UploadFile,name: str, user=UserSchema):
    data = await file.read()
    df = pandas.read_csv(io.BytesIO(data))
    if name == "ACTIVITY":
        activity(df, user)
    elif name == "SLEEP":
        sleep(df, user)
    elif name == "HEARTRATE_AUTO":
        heartrate_auto(df, user)
    elif name == "SPORT":
        sport(df, user)
    elif name == "ACTIVITY_STAGE":
        activity_stage(df, user)


def activity(df: pandas.DataFrame, user: User):
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


def sleep(df: pandas.DataFrame, user: User):
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


def heartrate_auto(df: pandas.DataFrame, user: User):
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


def sport(df: pandas.DataFrame, user: User):
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


def activity_stage(df: pandas.DataFrame, user: User):
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
