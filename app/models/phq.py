from mongoengine import CASCADE, Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    BooleanField,
    DateField,
    DateTimeField,
    DictField,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ReferenceField,
)

from app.models.user import User


class Phq(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    datetime = DateTimeField(required=True)
    answers = DictField(required=True)


class SingleQuestionAvgScore(EmbeddedDocument):
    average = FloatField(required=True)
    total_records = IntField(required=True)


class AvgAndEstimatedPhqScore(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = DateField(required=True)
    fixed = BooleanField(required=True)

    average_scores = DictField(
        child=EmbeddedDocumentField(SingleQuestionAvgScore), required=True
    )

    estimated_phq = FloatField(required=True)
