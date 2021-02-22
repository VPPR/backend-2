from fastapi import APIRouter, File, UploadFile, Body, Depends, HTTPException, status
from app.core.security import get_current_user
import io
import pandas

from zipfile import ZipFile

router = APIRouter()


@router.post("/miband/zip")
async def upload_zip(
    file: UploadFile = File(...),
    zip_password: str = Body(...),
    user=Depends(get_current_user),
):
    file = await file.read()
    zipfile = ZipFile(io.BytesIO(file))
    for i in zipfile.namelist():
        folder, filename = i.split("/")
        if filename:
            print(folder, filename)
            try:
                fileobj = zipfile.read(
                    name=folder + "/" + filename, pwd=bytes(zip_password, encoding="UTF-8")
                )
            except RuntimeError as e:
                # why 422 status code? read following
                # https://stackoverflow.com/questions/7939137/right-http-status-code-to-wrong-input
                # https://www.bennadel.com/blog/2434-http-status-codes-for-invalid-data-400-vs-422.htm
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="wrong password for zip file",
                )
            df = pandas.read_csv(io.BytesIO(fileobj))
            data = df.to_dict("records")