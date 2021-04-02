from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from app.api.api_v1.api import api_router
from app.core.config import settings

connect(host=settings.MONGO_DETAILS)

app = FastAPI(title="VPPR Depression Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
