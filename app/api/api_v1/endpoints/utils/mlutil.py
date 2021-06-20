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
