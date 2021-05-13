import random
from datetime import date, datetime, timedelta, timezone
from typing import List

from fastapi.exceptions import HTTPException
from starlette import status

from app.models.phq import AvgAndEstimatedPhqScore, Phq, SingleQuestionAvgScore
from app.models.user import User
from app.schema.phq import (
    GraphEntry,
    Question,
    SingleQuestionResponse,
    SingleQuestionResponseFloat,
)

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
    # record = AvgAndEstimatedPhqScore.objects(user=user).first()
    record = (
        Phq.objects(
            user=user,
        )
        .order_by("+datetime")
        .first()
    )
    if record:
        if record.datetime.date() == datetime.now(tz=timezone.utc).date():
            return []

    # get records for current user that have datetime greater than or equal to todays date at midnight
    # sort the records in desc order of datetime
    todays_records = Phq.objects(
        user=user,
        datetime__gte=datetime.combine(datetime.now().date(), datetime.min.time()),
    ).order_by("-datetime")
    all_ques = all_questions(user)
    # if no records for that day, send 3 random questions
    if len(todays_records) == 0:
        return random.sample(list(all_ques), k=3)
    if len(todays_records) < 3:
        # if no records past 4 hour, select 3 random questions
        if (
            datetime.now(tz=timezone.utc) - todays_records[0].datetime
        ).total_seconds() / 60 > 0.5:
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


def update_avg_and_estm_phq(
    user: User,
    body: list,
    date: date = datetime.now(tz=timezone.utc).date(),
    fixed=False,
):
    # update the average of each question and the estimated phq after each response

    if not body:
        # if no records for that day, update fixed value only
        # should only run when fix function is called
        that_days_record = AvgAndEstimatedPhqScore.objects(user=user, date=date).first()
        that_days_record.fixed = fixed
        that_days_record.save()
        return

    # fetch all records in desc order of date so 1st record will be latest
    all_records = AvgAndEstimatedPhqScore.objects(user=user).order_by("-date")
    todays_record = None
    if all_records:
        if all_records[0].date == date:
            todays_record = all_records[0]
    # if record for that day exists, update that record
    if todays_record:
        for response in body:
            # update values for all questions present in body
            qno = str(response.qno)
            score = get_score(response)
            old_avg = todays_record.average_scores.get(qno).average
            old_total_records = todays_record.average_scores.get(qno).total_records
            todays_record.estimated_phq += score - old_avg
            new_entry = SingleQuestionAvgScore(
                average=(old_avg * old_total_records + score) / (old_total_records + 1),
                total_records=old_total_records + 1,
            )
            todays_record.average_scores.update({qno: new_entry})
            todays_record.fixed = fixed
        # save the updated record
        todays_record.save()

    # if record for that day doesn't exists but their are previous records
    # in that case, we take latest record because if todays record doesn't exists, latest record gonna be yesterdays
    # and create new record for current day using yesterdays record and form values
    # assuming that we are running fix records function before this function on post request
    elif all_records:
        yesterdays_record = all_records[0]
        estimated_phq = yesterdays_record.estimated_phq
        average_scores = yesterdays_record.average_scores.copy()
        for response in body:
            qno = str(response.qno)
            score = get_score(response)
            yesterdays_avg = yesterdays_record.average_scores.get(qno).average
            yesterdays_total_records = yesterdays_record.average_scores.get(
                qno
            ).total_records
            estimated_phq += score - yesterdays_avg
            todays_entry = SingleQuestionAvgScore(
                average=(yesterdays_avg * yesterdays_total_records + score)
                / (yesterdays_total_records + 1),
                total_records=yesterdays_total_records + 1,
            )
            average_scores.update({qno: todays_entry})

        new_record = AvgAndEstimatedPhqScore(
            user=user,
            date=date,
            fixed=fixed,
            average_scores=average_scores,
            estimated_phq=estimated_phq,
        )

        # add this new record to db
        new_record.save()

    # if no record for user exists, first record is created
    # create new record
    else:
        average_scores = {}
        estimated_phq = 0
        for response in body:
            qno = str(response.qno)
            score = get_score(response)
            todays_entry = SingleQuestionAvgScore(average=score, total_records=1)
            estimated_phq += score
            average_scores.update({qno: todays_entry})
        new_record = AvgAndEstimatedPhqScore(
            user=user,
            date=date,
            fixed=fixed,
            average_scores=average_scores,
            estimated_phq=estimated_phq,
        )
        new_record.save()


def fix_missing_records(user, last_fix_date: date):
    # this function should take care of user not inputting all three records a day
    # as well as question not being asked single time for given day

    def daterange(start_date, end_date):
        # returns the range of dates to iterate on
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    for day in daterange(last_fix_date, datetime.now(tz=timezone.utc).date()):
        # fetch the records of particular day
        # check for the questiions that haven't answered at all in that days records
        # and create entry for those missing questions using previous day's average
        records = Phq.objects(
            user=user,
            datetime__gte=datetime.combine(day, datetime.min.time()),
            datetime__lt=datetime.combine(day + timedelta(days=1), datetime.min.time()),
        )
        estimated_phq_record = AvgAndEstimatedPhqScore.objects(
            user=user, date=last_fix_date
        ).first()

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

        update_avg_and_estm_phq(user, entry, day, fixed=True)


def generate_graph_values(user: User) -> List[GraphEntry]:
    graph_details = []
    records = AvgAndEstimatedPhqScore.objects(user=user).order_by("+date")
    # if no records, raise exception
    if records is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found 😞",
        )

    phq_records = list(Phq.objects(user=user).order_by("+date"))
    for record in records:
        sum_of_avg = 0
        q9_sum = 0
        q9_count = 0
        for i in range(1, 10):
            sum_of_avg += record.average_scores.get(str(i)).average
        for i in range(3):
            # check the 1st three records of phq table in ascending order of date
            #  if record has same date as average table record, calculate q9 average of that day
            # otherwise keep it 0
            if phq_records[0].datetime.date() == record.date:
                if (score := phq_records[0].answers.get("9")) is not None:
                    q9_sum += score
                    q9_count += 1
                # remove record that has been used so next record become 1st
                phq_records.pop(0)
            else:
                break
        graph_details.append(
            GraphEntry(
                date=record.date,
                estimated_phq=record.estimated_phq,
                sum_of_avg=sum_of_avg,
                q9_avg=(q9_sum / q9_count) if q9_count != 0 else 0,
            )
        )
    return graph_details
