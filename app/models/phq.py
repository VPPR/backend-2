from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    DictField,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ReferenceField,
)

from app.models.user import User


class Phq(Document):
    user = ReferenceField(User)
    datetime = DateTimeField(required=True)
    answers = DictField(required=True)


class SingleQuestionAvgScore(EmbeddedDocument):
    average = FloatField(required=True)
    total_records = IntField(required=True)


class AvgAndEstimatedPhqScore(Document):
    user = ReferenceField(User)
    first_recorded = DateTimeField(required=True)
    last_updated = DateTimeField(required=True)
    last_fixed = DateTimeField(required=True)

    average_scores = DictField(
        child=EmbeddedDocumentField(SingleQuestionAvgScore), required=True
    )

    estimated_phq = FloatField(required=True)
