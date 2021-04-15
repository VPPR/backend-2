import io
from typing import List
from zipfile import ZipFile

from asyncio import create_task
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
                except RuntimeError as e:
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

@router.post("/activity",status_code=200)
async def read_activity_csv(file: UploadFile = File(...), user = Depends(get_current_user)):
    file_data =await file.read()
    df = pandas.read_csv(io.BytesIO(file_data))
    print(df.head())

@router.post("/upload",status_code=200)
async def upload_file(
    user = Depends(get_current_user),
    activity: UploadFile = File(None,alias="ACTIVITY"),
    heartRateAuto: UploadFile = File(None,alias="HEARTRATE_AUTO"),
    sleep: UploadFile = File(None,alias="SLEEP"),
    actvityStage: UploadFile = File(None,alias="ACTIVITY_STAGE"),
    sport: UploadFile = File(None,alias="SPORT")
):
    if activity is not None:
        create_task(ziputils.parse_data(activity,"ACTIVITY",user))
    if heartRateAuto is not None:
        create_task(ziputils.parse_data(heartRateAuto,"HEARTRATE_AUTO",user))
    if sleep is not None:
        create_task(ziputils.parse_data(sleep,"SLEEP",user))
    if actvityStage is not None:
        create_task(ziputils.parse_data(actvityStage,"ACTIVITY_STAGE",user))
    if sport is not None:
        create_task(ziputils.parse_data(sport,"SPORT",user))
