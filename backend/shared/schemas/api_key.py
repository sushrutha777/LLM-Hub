from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class APIKeyBase(BaseModel):
    name: str

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyInDBBase(APIKeyBase):
    id: int
    key: str
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class APIKey(APIKeyInDBBase):
    pass
