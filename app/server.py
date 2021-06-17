from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from app.api.api_v1.api import api_router
from app.core.config import settings

connect(host=settings.MONGO_DETAILS, tz_aware=True)

app = FastAPI(
    title="VPPR Depression Detection",
    description='backend api for a depression detection system. Source code available <a href="https://github.com/VPPR/backend-2">here</a>',
    docs_url="/",
    redoc_url=None,
    debug=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
