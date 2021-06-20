from mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    FloatField,
    IntField,
    LongField,
    ReferenceField,
)

from app.models.user import User


class Predictions(Document):
    user = ReferenceField(User)
    start_time = LongField(required=True)
    end_time = IntField(required=True)
    sd_1 = FloatField(required=True)
    sd_2 = FloatField(required=True)
    depressed = BooleanField(required=True)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {
                "fields": ("user", "start_time"),
                "unique": True,
                "name": "user_start_time",
            },
            {"fields": ("user", "end_time"), "unique": True, "name": "user_end_time"},
            {
                "fields": ("user", "start_time", "end_time"),
                "unique": True,
                "name": "user_start_and_end_time",
            },
        ],
    }
