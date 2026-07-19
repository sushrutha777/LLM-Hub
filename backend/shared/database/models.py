from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from shared.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(String, primary_key=True, index=True) # e.g., 'openai'
    name = Column(String, nullable=False)             # e.g., 'OpenAI'
    description = Column(String, default="")
    color = Column(String, default="#ffffff")
    api_key = Column(String, nullable=True)           # Encrypted in production, plain for now
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    models = relationship("LLMModel", back_populates="provider")

class LLMModel(Base):
    __tablename__ = "models"
    
    id = Column(String, primary_key=True, index=True) # e.g., 'gpt-4o'
    provider_id = Column(String, ForeignKey("providers.id"))
    name = Column(String, nullable=False)             # e.g., 'GPT-4 Omni'
    best_for = Column(String, default="")
    is_active = Column(Boolean, default=True)
    free_tier = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    provider = relationship("Provider", back_populates="models")

class AIProfile(Base):
    __tablename__ = "ai_profiles"
    
    id = Column(String, primary_key=True, index=True) # e.g. 'rag-chat'
    name = Column(String, nullable=False)             # e.g. 'RAG Chat'
    description = Column(String, default="")
    model_id = Column(String, nullable=False)         # e.g. 'gemini-1.5-flash'
    provider_id = Column(String, nullable=False)      # e.g. 'google'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

