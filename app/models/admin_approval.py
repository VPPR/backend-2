from mongoengine import Document
from mongoengine.fields import ReferenceField
from .user import User
from bson.json_util import dumps


class Approval(Document):
    user = ReferenceField(User)
