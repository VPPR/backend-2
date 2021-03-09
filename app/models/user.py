from mongoengine import Document, StringField, EmailField, BooleanField
from mongoengine.errors import ValidationError


def is_phone_number(phone: str):
    if (
        not phone.isnumeric()
        or not phone.startswith(("6", "7", "8", "9"))
        or not len(phone) == 10
    ):
        raise ValidationError("Not a valid phone number")


class User(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField(validation=is_phone_number)
    is_admin = BooleanField(required=True)
    password = StringField(required=True)
    is_active = BooleanField(default=False)
