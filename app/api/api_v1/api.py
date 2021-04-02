from fastapi import APIRouter
from app.api.api_v1.endpoints import approvals, login, user, zip
api_router = APIRouter()


api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["Approval"])
api_router.include_router(zip.router, prefix="/", tags=["zip"])

