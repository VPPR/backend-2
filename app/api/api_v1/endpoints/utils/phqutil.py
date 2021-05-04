import random
from datetime import datetime, timezone
from typing import Dict, List

from fastapi.param_functions import Body

from app.models.phq import Phq
from app.models.user import User
from app.schema.phq import SingleQuestionResponce

QV1 = [
    "I have little interest or pleasure in doing things",
    "I feel down and depressed and hopeless",
    "I have trouble with sleep",
    "I have been feeling tired and have little energy",
    "I have a poor appetite or am overeating",
    "I feel guilty or bad about myself",
    "I have trouble concentrating",
    "I am moving slower or fidgeting more",
    "I would be better off dead or hurting myself",
]
QV2 = [
    "I have lots of interest or pleasure in doing things",
    "I feel up and bright and hopeful",
    "I have been sleeping well",
    "I have been feeling active and have lots of enery",
    "I am eating the right amount of food",
    "I feel positive and good about myself",
    "I can concentrate well",
    "I am not fidgety or feel weighed down either",
    "I do not want to hurt or kill myself",
]


def all_questions() -> list:
    questions = {}
    for i in range(0, 9):
        version = random.choice([1, 2])
        question = ""
        if version == 1:
            question = QV1[i]
        else:
            question = QV2[i]
        questions[i + 1] = {"question": question, "version": version}
    return questions


def three_questions(user: User) -> list:
    # get records for current user that have datetime greater than or equal to todays date at midnight
    # sort the records in desc order of datetime
    todays_records = Phq.objects(
        user=user,
        datetime__gte=datetime.combine(datetime.utcnow().date(), datetime.min.time()),
    ).order_by("-datetime")
    all_ques = all_questions()
    # if no records for that day, send 3 random questions
    if len(todays_records) == 0:
        return dict(random.choices(list(all_ques.items()), k=3))
    if len(todays_records) < 3:
        # if no records past 4 hour, select 3 random questions
        if (datetime.utcnow() - todays_records[0].datetime).total_seconds() / 60 > 240:
            return dict(random.choices(list(all_ques.items()), k=3))
    return []


def add_answers_to_db(user: User, body: Body):
    def get_score(response: SingleQuestionResponce):
        if response:
            if response.version == 1:
                return response.score
            elif response.version == 2:
                return 3 - response.score

    phq = Phq(
        user=user,
        datetime=datetime.now(tz=timezone.utc),
        q1=get_score(body.get(1)),
        q2=get_score(body.get(2)),
        q3=get_score(body.get(3)),
        q4=get_score(body.get(4)),
        q5=get_score(body.get(5)),
        q6=get_score(body.get(6)),
        q7=get_score(body.get(7)),
        q8=get_score(body.get(8)),
        q9=get_score(body.get(9)),
    )
    phq.save()
