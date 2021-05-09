import random
from datetime import datetime, timedelta, timezone
from typing import List

from app.models.phq import AvgAndEstimatedPhqScore, Phq, SingleQuestionAvgScore
from app.models.user import User
from app.schema.phq import Question, SingleQuestionResponse, SingleQuestionResponseFloat

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


def all_questions(user: User) -> List[Question]:
    # returns the list of all questions
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    questions = []
    for i in range(0, 9):
        version = random.choice([1, 2])
        question = ""
        if version == 1:
            question = QV1[i]
        else:
            question = QV2[i]
        average_score = 0
        if record:
            average_score = record.average_scores.get(str(i + 1)).average
            if version == 2:
                average_score = 3 - average_score
            average_score = int(average_score)
        # questions.append([i+1, question, version, average_score])
        questions.append(
            {
                "qno": i + 1,
                "question": question,
                "version": version,
                "average_score": average_score,
            }
        )
    return questions


def three_questions(user: User) -> List[Question]:
    # if user has submitted his first record, then he won't get any more questions on same day
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record.first_recorded.date() == datetime.now(tz=timezone.utc).date():
        return []
    # get records for current user that have datetime greater than or equal to todays date at midnight
    # sort the records in desc order of datetime
    todays_records = Phq.objects(
        user=user,
        datetime__gte=datetime.combine(datetime.utcnow().date(), datetime.min.time()),
    ).order_by("-datetime")
    all_ques = all_questions(user)
    # if no records for that day, send 3 random questions
    if len(todays_records) == 0:
        return random.sample(list(all_ques), k=3)
    if len(todays_records) < 3:
        # if no records past 4 hour, select 3 random questions
        if (datetime.utcnow() - todays_records[0].datetime).total_seconds() / 60 > 0.5:
            return random.sample(list(all_ques), k=3)
    return []


def get_score(response: SingleQuestionResponse) -> int:
    # if question version was 1, return score as it is
    # if question version was 2, return 3-score
    if response:
        if response.version == 1:
            return response.score
        elif response.version == 2:
            return 3 - response.score


def add_answers_to_db(user: User, body: List[SingleQuestionResponse]):
    answers = {}
    for response in body:
        answers.update({str(response.qno): get_score(response)})
    phq = Phq(user=user, datetime=datetime.now(tz=timezone.utc), answers=answers)
    phq.save()


def update_avg_and_estm_phq(user: User, body: list):
    # update the average of each question and the estimated phq after each response
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    if record:
        # if record exists, update it

        # if new score come, update average
        # formula: new_avg = (old_avg * number_of_old_records + new record) / (number_of_old_records + 1)
        for response in body:
            previous_entry = record.average_scores.get(str(response.qno))
            new_entry = SingleQuestionAvgScore(
                average=(
                    previous_entry.average * previous_entry.total_records
                    + get_score(response)
                )
                / (previous_entry.total_records + 1),
                total_records=previous_entry.total_records + 1,
            )
            record.estimated_phq += get_score(response) - previous_entry.average
            record.average_scores.update({str(response.qno): new_entry})

        # update timestamp
        record.last_updated = datetime.now(tz=timezone.utc)
        # write changes to db
        record.save()

    else:
        # if record doesn't exists, create new record
        scores = {}
        for response in body:
            scores.update(
                {
                    str(response.qno): SingleQuestionAvgScore(
                        average=get_score(response), total_records=1
                    )
                }
            )
        record = AvgAndEstimatedPhqScore(
            user=user,
            first_recorded=datetime.now(tz=timezone.utc),
            last_updated=datetime.now(tz=timezone.utc),
            last_fixed=datetime.now(tz=timezone.utc),
            average_scores=scores,
            # this else case runs only for users first response
            # therefore estimated phq is just sum of all scores
            estimated_phq=sum(get_score(response) for response in body),
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

        entry = []

        for i in range(1, 10):
            entry_exists = False
            for record in records:
                if record.answers.get(str(i)) is not None:
                    entry_exists = True
            if not entry_exists:
                entry.append(
                    SingleQuestionResponseFloat(
                        qno=i,
                        score=estimated_phq_record.average_scores.get(str(i)).average,
                        version=1,
                    )
                )

        update_avg_and_estm_phq(user, entry)

    # update last fixed date
    record = AvgAndEstimatedPhqScore.objects(user=user).first()
    record.last_fixed = datetime.now(tz=timezone.utc)
    record.save()
