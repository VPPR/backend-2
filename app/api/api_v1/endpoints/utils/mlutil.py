import pandas

from app.models.gadgetbridge import Gadgetbridge
from app.models.predictions import Predictions
from app.models.user import User


def do_ml_stuff(user: User):
    # fetch start_time for latest prediction if present
    # order records in desc order and select first record. ez.
    latest_prediction = Predictions.objects(user=user).order_by("-start_time").first()

    # fetch records from gadgetbridge collection that have timestamp greater or equal to
    # start_time of latest prediction
    # if no prediction is present, fetch all records
    # and order it in increasing order by timestamp
    records = (
        Gadgetbridge.objects(
            user=user, timestamp__gte=latest_prediction.start_date
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
    generate_periods(df)


# this class cause i'mma just copy ipynb stuff without thinking too much
class HRVDuration:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish


def printPeriods(periods, df):
    print("________________________")
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
    print("________________________")


def generate_periods(df: pandas.DataFrame):
    periods = []
    d = HRVDuration(start=0, finish=0)
    k = 0
    while k < len(df):
        k = d.finish + 1
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
