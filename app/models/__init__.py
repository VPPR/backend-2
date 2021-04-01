from mongoengine import connect

from app.core.config import settings

connect(host=settings.MONGO_DETAILS)
