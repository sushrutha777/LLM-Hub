from sqlalchemy.orm import Session
from shared.database.models import APIKey
from shared.schemas.api_key import APIKeyCreate
import secrets

def create_api_key(db: Session, api_key_in: APIKeyCreate, user_id: int):
    raw_key = f"llmhub-{secrets.token_urlsafe(32)}"
    
    db_api_key = APIKey(
        key=raw_key,
        name=api_key_in.name,
        user_id=user_id
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def get_user_api_keys(db: Session, user_id: int):
    return db.query(APIKey).filter(APIKey.user_id == user_id).all()

def get_api_key(db: Session, key: str):
    return db.query(APIKey).filter(APIKey.key == key).first()
