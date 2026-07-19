from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utils.dependencies import get_db, get_current_active_user
from services import api_key_service
from shared.schemas.api_key import APIKey, APIKeyCreate
from shared.database.models import User as UserModel

router = APIRouter()

@router.post("/", response_model=APIKey)
def create_api_key(
    *,
    db: Session = Depends(get_db),
    api_key_in: APIKeyCreate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    api_key = api_key_service.create_api_key(db=db, api_key_in=api_key_in, user_id=current_user.id)
    return api_key

@router.get("/", response_model=List[APIKey])
def read_api_keys(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    return api_key_service.get_user_api_keys(db=db, user_id=current_user.id)
