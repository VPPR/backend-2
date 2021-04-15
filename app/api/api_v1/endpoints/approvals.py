from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.params import Path

from app.api.deps import get_current_admin
from app.models.admin_approval import Approval
from app.models.user import User
from app.schema.response import Response
from app.schema.user import User as UserSchema

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_approval_entries(user: User = Depends(get_current_admin)):
    return [f for f in Approval.objects().scalar("user")]


@router.get("/{id}", response_model=Response)
def approve_user_by_id(user: User = Depends(get_current_admin), id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Id"
        )
    approval = Approval.objects(user=id).first()
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No approval request found"
        )
    approved_user = approval.user
    if approved_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has privileges",
        )
    approved_user.is_active = True
    approved_user.save()
    approval.delete()
    return Response(message="User approved", detail=UserSchema.from_orm(approved_user))
