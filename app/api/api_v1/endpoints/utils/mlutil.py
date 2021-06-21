import pickle
from typing import List, Tuple

import numpy
import pandas
from pymongo.errors import BulkWriteError
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from app.models.gadgetbridge import Gadgetbridge
from app.models.prediction import Prediction
from app.models.user import User

# when you load model from pickle file, it needs the libraries to be imported
# but, since you are not creating the objects of this clasifiers,
# ./format will remove them while formatting, breaking the code
# bellow two lines prevent that from happening
_ = DecisionTreeClassifier()
_ = AdaBoostClassifier()


def do_ml_stuff(user: User):
    # fetch start_time for latest prediction if present
    # order records in desc order and select first record. ez.
    latest_prediction = Prediction.objects(user=user).order_by("-start_time").first()

    # fetch records from gadgetbridge collection that have timestamp greater or equal to
    # start_time of latest prediction
    # if no prediction is present, fetch all records
    # and order it in increasing order by timestamp
    records = (
        Gadgetbridge.objects(
            user=user, timestamp__gte=latest_prediction.start_time - 1
        ).order_by("+timestamp")
        if latest_prediction
        else Gadgetbridge.objects(user=user).order_by("+timestamp")
    )

    # delete latest prediction cause it is going to be predicted again anyways
    if latest_prediction:
        latest_prediction.delete()

    # convert records to list of tuples with only timestamp and heart_rate
    # then load that data to pandas dataframe so that operations from here onwards can be copy pasted
    # from depression.ipynb on google colab since it followes this dataframe format (but in upper case)
    df = pandas.DataFrame(
        records.values_list("timestamp", "heart_rate"),
        columns=["timestamp", "heart_rate"],
    )

    # following operations are copy pasted from depression.ipynb
    # to remove the obivious outliers
    df.drop(df[df["heart_rate"] == 255].index, inplace=True)
    df.drop(df[df["heart_rate"] == 0].index, inplace=True)
    df.drop(df[df["heart_rate"] == -1].index, inplace=True)
    df = df.reset_index()
    df = df.drop(columns=["index"])
    print(df)
    generate_periods(user, df)


# this class cause i'mma just copy ipynb stuff without thinking too much
class HRVDuration:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish


def printPeriods(periods, df):
    print("______Printng Periods_________")
    for i in range(0, len(periods)):
        # print(str(df.iloc[periods[i].start,0])+" ---> "+str(df.iloc[periods[i].finish,0]))
        print(
            str(
                pandas.to_datetime(df.iloc[periods[i].start, 0], unit="s")
                .tz_localize("UTC")
                .tz_convert("Asia/Kolkata")
            )
            + " ---> "
            + str(
                pandas.to_datetime(df.iloc[periods[i].finish, 0], unit="s")
                .tz_localize("UTC")
                .tz_convert("Asia/Kolkata")
            )
        )


def generate_periods(user: User, df: pandas.DataFrame):
    periods = []
    d = HRVDuration(start=0, finish=0)
    k = 0
    while k < len(df):
        k = d.finish
        for i in range(k, len(df) - 1):
            x0 = df.iloc[i, 0]
            y0 = df.iloc[i + 1, 0]
            if y0 - x0 < 30:
                d.start = i
                break
        for i in range(d.start, len(df) - 1):
            if df.iloc[i + 1, 0] - df.iloc[i, 0] < 30:
                d.finish = i + 1
            else:
                break
        if (len(periods) > 0 and periods[-1].finish != d.finish) or len(periods) == 0:
            if d.finish - d.start > 10:
                periods.append(HRVDuration(d.start, d.finish))
        else:
            break
    printPeriods(periods, df)
    calculate_sd_values(user, periods, df)


def bpm_to_rr(bpm):
    return 60000 / bpm


def calculate_sd_values(user: User, periods: List[HRVDuration], df: pandas.DataFrame):
    sd_values = []
    for p in periods:
        x = []
        y = []
        for t in range(p.start, p.finish - 1):
            x.append(bpm_to_rr(df.iloc[t, 1]))
            y.append(bpm_to_rr(df.iloc[t + 1, 1]))
        sd1 = numpy.sqrt(0.5) * numpy.std(numpy.array(y) - numpy.array(x))
        sd2 = numpy.sqrt(0.5) * numpy.std(numpy.array(y) + numpy.array(x))
        sd_values.append((sd1, sd2))
    predict_stuff_and_add_to_db(user, periods, df, sd_values)


def predict_stuff_and_add_to_db(
    user: User,
    periods: List[HRVDuration],
    df: pandas.DataFrame,
    sd_values: List[Tuple[float]],
):
    records = []
    model = pickle.load(open("model.sav", "rb"))
    for i in range(len(periods)):
        records.append(
            Prediction(
                user=user,
                start_time=df.iloc[periods[i].start, 0],
                end_time=df.iloc[periods[i].finish, 0],
                sd1=sd_values[i][0],
                sd2=sd_values[i][1],
                depressed=True
                if model.predict([[sd_values[i][0], sd_values[i][1]]]) == [1]
                else False,
            ).to_mongo()
        )
    print(
        "\n_____Print records after prediction____________________________________________"
    )
    for i in records:
        print(i)
    try:
        Prediction._get_collection().insert_many(records, ordered=False)
    except BulkWriteError:
        print(
            "Batch Inserted with some errors. May be some duplicates were found and are skipped."
        )
    except Exception as e:
        print({"error": str(e)})
