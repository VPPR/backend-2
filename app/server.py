from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.security import get_password_hash

connect(host=settings.MONGO_DETAILS)
from app.models.user import User

# User(fullname="Pranav Bakre",
#                 email="psbakre@yahoo.com",
#                 phone="9029050534",
#                 is_admin=True,
#                 password=get_password_hash("Praan123"),
#                 is_active=True).save()

app = FastAPI(title="VPPR Depression Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
