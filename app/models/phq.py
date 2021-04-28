from mongoengine import Document
from mongoengine.fields import DateTimeField, ReferenceField, IntField

from app.models.user import User


class Phq(Document):
    user = ReferenceField(User)
    date = DateTimeField(required=True)
    
    q1 = IntField(required=False)
    q2 = IntField(required=False)
    q3 = IntField(required=False)
    q4 = IntField(required=False)
    q5 = IntField(required=False)
    q6 = IntField(required=False)
    q7 = IntField(required=False)
    q8 = IntField(required=False)
    q9 = IntField(required=False)

