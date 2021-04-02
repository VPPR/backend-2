import io
from zipfile import ZipFile

import pandas
import pyzipper
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status

from app.api.api_v1.endpoints.utils import ziputils
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/miband/zip")
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
                    print(e.with_traceback())
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
