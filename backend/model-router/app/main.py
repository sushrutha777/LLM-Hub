from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
from routes import chat

app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Model Router",
    description="Internal microservice handling LLM provider routing.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "model-router healthy"}

# Note: We expose this at /v1 to mimic OpenAI
app.include_router(chat.router, prefix="/v1", tags=["chat"])
