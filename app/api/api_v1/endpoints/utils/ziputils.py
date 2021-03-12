import pandas
from app.models.zip import Activity, ActivityStage, HeartrateAuto, Sleep, Sport
from app.models.user import User


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
        records.append(activity)
    Activity.objects.insert(records)


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
        records.append(sleep)
    Sleep.objects.insert(records)


def heartrate_auto(df: pandas.DataFrame, user: User):
    records = []
    for record in df.to_dict("records"):
        heartrate_auto = HeartrateAuto(
            date=record.get("date"),
            time=record.get("time"),
            heart_rate=record.get("heartRate"),
            user=user,
        )
        records.append(heartrate_auto)
    HeartrateAuto.objects.insert(records)


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
        records.append(sport)
    Sport.objects.insert(records)


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
        records.append(activity_stage)
    ActivityStage.objects.insert(records)
