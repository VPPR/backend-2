import random
from datetime import datetime, timedelta, timezone

from fastapi.param_functions import Body

from app.models.phq import AvgAndEstimatedPhqScore, Phq, SingleQuestionAvgScore
from app.models.user import User
from app.schema.phq import SingleQuestionResponce, SingleQuestionResponceFloat

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
    # returns the list of all questions and their versions
    # return : [{1: {"question" : <question string>, "version" : <int 1 or 2>}, 2 : {}, ..., 9{}}]
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


def three_questions(user: User) -> dict:
    # get records for current user that have datetime greater than or equal to todays date at midnight
    # sort the records in desc order of datetime
    todays_records = Phq.objects(
        user=user,
        datetime__gte=datetime.combine(datetime.utcnow().date(), datetime.min.time()),
    ).order_by("-datetime")
    all_ques = all_questions()
    # if no records for that day, send 3 random questions
    if len(todays_records) == 0:
        questions_three = random.sample(list(all_ques.items()), k=3)
        return dict(questions_three)
    if len(todays_records) < 3:
        # if no records past 4 hour, select 3 random questions
        if (datetime.utcnow() - todays_records[0].datetime).total_seconds() / 60 > 240:
            questions_three = random.sample(list(all_ques.items()), k=3)
            return dict(questions_three)
    return {}


def get_score(response: SingleQuestionResponce):
    # if question version was 1, return score as it is
    # if question version was 2, return 3-score
    if response:
        if response.version == 1:
            return response.score
        elif response.version == 2:
            return 3 - response.score


def add_answers_to_db(user: User, body: Body):
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


def update_avg_and_estm_phq(user: User, body: dict):
    # update the average of each question and the estimated phq after each response
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record:
        # if record exists, update it

        # if new score come, update average
        # formula: new_avg = (old_avg * number_of_old_records + new record) / (number_of_old_records + 1)
        if q := body.get(1):
            record.estimated_phq += get_score(q) - record.q1.average
            record.q1.average = (
                record.q1.average * record.q1.total_records + get_score(q)
            ) / (record.q1.total_records + 1)
            record.q1.total_records += 1
        if q := body.get(2):
            record.estimated_phq += get_score(q) - record.q2.average
            record.q2.average = (
                record.q2.average * record.q2.total_records + get_score(q)
            ) / (record.q2.total_records + 1)
            record.q2.total_records += 1
        if q := body.get(3):
            record.estimated_phq += get_score(q) - record.q3.average
            record.q3.average = (
                record.q3.average * record.q3.total_records + get_score(q)
            ) / (record.q3.total_records + 1)
            record.q3.total_records += 1
        if q := body.get(4):
            record.estimated_phq += get_score(q) - record.q4.average
            record.q4.average = (
                record.q4.average * record.q4.total_records + get_score(q)
            ) / (record.q4.total_records + 1)
            record.q4.total_records += 1
        if q := body.get(5):
            record.estimated_phq += get_score(q) - record.q5.average
            record.q5.average = (
                record.q5.average * record.q5.total_records + get_score(q)
            ) / (record.q5.total_records + 1)
            record.q5.total_records += 1
        if q := body.get(6):
            record.estimated_phq += get_score(q) - record.q6.average
            record.q6.average = (
                record.q6.average * record.q6.total_records + get_score(q)
            ) / (record.q6.total_records + 1)
            record.q6.total_records += 1
        if q := body.get(7):
            record.estimated_phq += get_score(q) - record.q7.average
            record.q7.average = (
                record.q7.average * record.q7.total_records + get_score(q)
            ) / (record.q7.total_records + 1)
            record.q7.total_records += 1
        if q := body.get(8):
            record.estimated_phq += get_score(q) - record.q8.average
            record.q8.average = (
                record.q8.average * record.q8.total_records + get_score(q)
            ) / (record.q8.total_records + 1)
            record.q8.total_records += 1
        if q := body.get(9):
            record.estimated_phq += get_score(q) - record.q9.average
            record.q9.average = (
                record.q9.average * record.q9.total_records + get_score(q)
            ) / (record.q9.total_records + 1)
            record.q9.total_records += 1

        # update timestamp
        record.last_updated = datetime.now(tz=timezone.utc)
        # write changes to db
        record.save()

    else:
        # if record doesn't exists, create new record
        record = AvgAndEstimatedPhqScore(
            user=user,
            last_updated=datetime.now(tz=timezone.utc),
            last_fixed=datetime.now(tz=timezone.utc),
            q1=SingleQuestionAvgScore(average=get_score(body.get(1)), total_records=1),
            q2=SingleQuestionAvgScore(average=get_score(body.get(2)), total_records=1),
            q3=SingleQuestionAvgScore(average=get_score(body.get(3)), total_records=1),
            q4=SingleQuestionAvgScore(average=get_score(body.get(4)), total_records=1),
            q5=SingleQuestionAvgScore(average=get_score(body.get(5)), total_records=1),
            q6=SingleQuestionAvgScore(average=get_score(body.get(6)), total_records=1),
            q7=SingleQuestionAvgScore(average=get_score(body.get(7)), total_records=1),
            q8=SingleQuestionAvgScore(average=get_score(body.get(8)), total_records=1),
            q9=SingleQuestionAvgScore(average=get_score(body.get(9)), total_records=1),
            # this else case runs only for users first response
            # therefore estimated phq is just sum of all scores
            estimated_phq=sum(get_score(v) for _, v in body.items()),
        )
        record.save()


def fix_missing_records(user, last_fix_date: datetime):
    # this function should take care of user not inputting all three records a day
    # as well as question not being asked single time for given day

    def daterange(start_date, end_date):
        # returns the range of dates to iterate on
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    for day in daterange(last_fix_date.date(), datetime.now(tz=timezone.utc).date()):
        # fetch the records of particular day
        # check for the questiions that haven't answered at all in that days records
        # and create entry for those missing questions using previous day's average
        records = Phq.objects(
            user=user,
            datetime__gte=datetime.combine(day, datetime.min.time()),
            datetime__lt=datetime.combine(day + timedelta(days=1), datetime.min.time()),
        )
        estimated_phq_record = AvgAndEstimatedPhqScore.objects(user=user).first()

        entry = {}

        entry_exists = False
        for record in records:
            if record.q1 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[1] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q1.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q2 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[2] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q2.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q3 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[3] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q3.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q4 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[4] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q4.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q5 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[5] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q5.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q6 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[6] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q6.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q7 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[7] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q7.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q8 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[8] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q8.average, version=1
            )

        entry_exists = False
        for record in records:
            if record.q9 is not None:
                entry_exists = True
                break
        if not entry_exists:
            entry[9] = SingleQuestionResponceFloat(
                score=estimated_phq_record.q9.average, version=1
            )
        update_avg_and_estm_phq(user, entry)

    # update last fixed date
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    record.last_fixed = datetime.now(tz=timezone.utc)
    record.save()
