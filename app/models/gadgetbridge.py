from mongoengine import Document
from mongoengine.fields import IntField, LongField, ReferenceField

from app.models.user import User


class Gadgetbridge(Document):
    user = ReferenceField(User)
    timestamp = LongField(required=True)
    heart_rate = IntField(required=True)

    meta = {
        "index_background": True,
        "indexes": [
            "user",
            {"fields": ("user", "timestamp"), "unique": True, "name": "user_timestamp"},
        ],
    }
