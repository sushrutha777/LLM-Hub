from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from shared.database.session import SessionLocal
from shared.database.models import AIProfile
import redis.asyncio as redis
from shared.config.settings import settings

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class AIProfileBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    model_id: str
    provider_id: str
    is_active: Optional[bool] = True

class AIProfileCreate(AIProfileBase):
    pass

class AIProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_id: Optional[str] = None
    provider_id: Optional[str] = None
    is_active: Optional[bool] = None

class AIProfileResponse(AIProfileBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

async def invalidate_cache(profile_id: str):
    try:
        await redis_client.delete(f"profile:{profile_id}")
    except Exception as e:
        import logging
        logging.error(f"Error invalidating Redis cache for profile {profile_id}: {e}")

@router.get("/", response_model=List[AIProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    return db.query(AIProfile).all()

@router.post("/", response_model=AIProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile_in: AIProfileCreate, db: Session = Depends(get_db)):
    # Check if profile already exists
    existing = db.query(AIProfile).filter(AIProfile.id == profile_in.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"AI Profile with ID '{profile_in.id}' already exists")
    
    db_profile = AIProfile(**profile_in.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    # Invalidate cache
    await invalidate_cache(db_profile.id)
    
    return db_profile

@router.put("/{profile_id}", response_model=AIProfileResponse)
async def update_profile(profile_id: str, profile_in: AIProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(AIProfile).filter(AIProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="AI Profile not found")
    
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    
    # Invalidate cache
    await invalidate_cache(profile_id)
    
    return db_profile

@router.delete("/{profile_id}")
async def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    db_profile = db.query(AIProfile).filter(AIProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="AI Profile not found")
    
    db.delete(db_profile)
    db.commit()
    
    # Invalidate cache
    await invalidate_cache(profile_id)
    
    return {"success": True}
