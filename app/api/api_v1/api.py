from fastapi import APIRouter
from .endpoints.login import router as login_router
from .endpoints.zip import router as zip_router

api_router = APIRouter()


api_router.include_router(login_router, tags=['users'])
api_router.include_router(zip_router, tags=['zip'])