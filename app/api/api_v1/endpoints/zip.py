import io
from asyncio import create_task
from zipfile import ZipFile

import pandas
import pyzipper
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status

from app.api.api_v1.endpoints.utils import ziputils
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/zip")
async def upload_zip(
    file: UploadFile = File(...),
    zip_password: str = Body(...),
    user=Depends(get_current_user),
):
    file = await file.read()
    zipfile = ZipFile(io.BytesIO(file))
    with pyzipper.AESZipFile(io.BytesIO(file)) as f:
        f.pwd = bytes(zip_password, encoding="UTF-8")
        for i in zipfile.namelist():
            folder, filename = i.split("/")
            if folder in ["ACTIVITY_MINUTE", "BODY", "HEARTRATE", "USER"]:
                continue
            if filename:
                try:
                    fileobj = f.read(folder + "/" + filename)
                except RuntimeError:
                    # why 422 status code? read following
                    # https://stackoverflow.com/questions/7939137/right-http-status-code-to-wrong-input
                    # https://www.bennadel.com/blog/2434-http-status-codes-for-invalid-data-400-vs-422.htm
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="wrong password for zip file",
                    )
                df = pandas.read_csv(io.BytesIO(fileobj))
                if folder == "ACTIVITY":
                    ziputils.activity(df, user)
                elif folder == "SLEEP":
                    ziputils.sleep(df, user)
                elif folder == "HEARTRATE_AUTO":
                    ziputils.heartrate_auto(df, user)
                elif folder == "SPORT":
                    ziputils.sport(df, user)
                elif folder == "ACTIVITY_STAGE":
                    ziputils.activity_stage(df, user)


@router.post("/upload", status_code=200)
async def upload_file(
    user=Depends(get_current_user),
    activity: UploadFile = File(None, alias="ACTIVITY"),
    heartrate_auto: UploadFile = File(None, alias="HEARTRATE_AUTO"),
    sleep: UploadFile = File(None, alias="SLEEP"),
    activity_stage: UploadFile = File(None, alias="ACTIVITY_STAGE"),
    sport: UploadFile = File(None, alias="SPORT"),
    gadgetbridge: UploadFile = File(None, alias="GADGETBRIDGE"),
):
    async def get_df(file: UploadFile):
        return pandas.read_csv(io.BytesIO(await file.read()))

    if activity:
        create_task(ziputils.activity(await get_df(activity), user))
    if heartrate_auto:
        create_task(ziputils.heartrate_auto(await get_df(heartrate_auto), user))
    if sleep:
        create_task(ziputils.sleep(await get_df(sleep), user))
    if activity_stage:
        create_task(ziputils.activity_stage(await get_df(activity_stage), user))
    if sport:
        create_task(ziputils.sport(await get_df(sport), user))
    if gadgetbridge:
        create_task(ziputils.gadgetbridge(gadgetbridge, user))
