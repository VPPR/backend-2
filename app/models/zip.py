from mongoengine import CASCADE, Document
from mongoengine.fields import (
    FloatField,
    IntField,
    LongField,
    ReferenceField,
    StringField,
)

from app.models.user import User


class Activity(Document):
    date = StringField(required=True)
    steps = IntField(required=True)
    distance = IntField(required=True)
    run_distance = IntField(required=True)
    calories = IntField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {"fields": ("user", "date"), "unique": True, "name": "user_date"},
        ],
    }


class Sleep(Document):
    date = StringField(required=True)
    deep_sleep_time = IntField(required=True)
    shallow_sleep_time = IntField(required=True)
    wake_time = IntField(required=True)
    sleep_start_time = LongField(required=True)
    sleep_stop_time = LongField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {"fields": ("user", "date"), "unique": True, "name": "user_date"},
        ],
    }


class Sport(Document):
    sport_type = IntField(required=True)
    start_time = LongField(required=True)
    sport_time = IntField(required=True)
    distance = FloatField(required=True)
    max_pace = FloatField(required=True)
    min_pace = FloatField(required=True)
    avg_pace = FloatField(required=True)
    calories = IntField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {
                "fields": ("user", "start_time"),
                "unique": True,
                "name": "user_start_time",
            },
        ],
    }


class ActivityStage(Document):
    date = StringField(required=True)
    activity_start_time = StringField(required=True)
    activity_stop_time = StringField(required=True)
    distance = IntField(required=True)
    calories = IntField(required=True)
    steps = IntField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {
                "fields": ("user", "date", "activity_start_time"),
                "unique": True,
                "name": "user_date_activity_start_time",
            },
        ],
    }


class HeartrateAuto(Document):
    date = StringField(required=True)
    time = StringField(required=True)
    heart_rate = IntField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {
                "fields": ("user", "date", "time"),
                "unique": True,
                "name": "user_date_time",
            },
        ],
    }
