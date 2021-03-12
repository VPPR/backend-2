from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    MONGO_DETAILS: str = config("MONGO_DETAILS")
    TOKEN_EXPIRY: int = config("TOKEN_EXPIRY")
    ALGORITHM: str = "HS256"
    SECRET_KEY = config("SECRET_KEY")


settings = Settings()
