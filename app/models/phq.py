from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ReferenceField,
)

from app.models.user import User


class Phq(Document):
    user = ReferenceField(User)
    datetime = DateTimeField(required=True)

    q1 = IntField(required=False)
    q2 = IntField(required=False)
    q3 = IntField(required=False)
    q4 = IntField(required=False)
    q5 = IntField(required=False)
    q6 = IntField(required=False)
    q7 = IntField(required=False)
    q8 = IntField(required=False)
    q9 = IntField(required=False)


class SingleQuestionAvgScore(EmbeddedDocument):
    average = FloatField(required=True)
    total_records = IntField(required=True)


class AvgAndEstimatedPhqScore(Document):
    user = ReferenceField(User)
    first_recorded = DateTimeField(required=True)
    last_updated = DateTimeField(required=True)
    last_fixed = DateTimeField(required=True)

    q1 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q2 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q3 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q4 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q5 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q6 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q7 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q8 = EmbeddedDocumentField(SingleQuestionAvgScore)
    q9 = EmbeddedDocumentField(SingleQuestionAvgScore)

    estimated_phq = FloatField(required=True)
