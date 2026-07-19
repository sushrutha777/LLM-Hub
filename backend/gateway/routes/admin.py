import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from shared.database.session import SessionLocal
from shared.database.models import APIKey, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str

class CreateKeyRequest(BaseModel):
    name: str

@router.get("/keys", response_model=List[APIKeyResponse])
def list_keys(db: Session = Depends(get_db)):
    # For phase 4, we bypass real user auth on the admin panel and just fetch all keys
    keys = db.query(APIKey).all()
    return [{"id": k.id, "key": k.key, "name": k.name} for k in keys]

@router.post("/keys", response_model=APIKeyResponse)
def create_key(req: CreateKeyRequest, db: Session = Depends(get_db)):
    # Ensure there's a default user for our keys
    user = db.query(User).first()
    if not user:
        user = User(email="admin@llmhub.internal", hashed_password="hashed")
        db.add(user)
        db.commit()
        db.refresh(user)

    new_key = f"llmhub-{uuid.uuid4().hex}"
    
    api_key = APIKey(
        key=new_key,
        name=req.name,
        user_id=user.id
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return {"id": api_key.id, "key": api_key.key, "name": api_key.name}

@router.delete("/keys/{key_id}")
def delete_key(key_id: int, db: Session = Depends(get_db)):
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
        
    db.delete(key)
    db.commit()
    return {"success": True}
