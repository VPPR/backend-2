from mongoengine import Document
from mongoengine.fields import ReferenceField
from .user import User


class Approval(Document):
    user = ReferenceField(User)
