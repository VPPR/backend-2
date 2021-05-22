from mongoengine import CASCADE, Document
from mongoengine.fields import ReferenceField

from .user import User


class Approval(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
