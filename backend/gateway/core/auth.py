from fastapi import Request, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from shared.database.session import SessionLocal
from shared.database.models import APIKey
from core.rate_limit import check_rate_limit

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(request: Request, api_key_header: str = Security(api_key_header), db: Session = Depends(get_db)):
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    if api_key_header.startswith("Bearer "):
        api_key_header = api_key_header[7:]

    # For Phase 1 we query the database directly. In Phase 2 we will use Redis cache here.
    db_key = db.query(APIKey).filter(APIKey.key == api_key_header).first()
    if not db_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    # Check rate limit (60 req / min)
    await check_rate_limit(db_key.key, limit=60, window=60)
    
    return db_key
