from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
from routes import proxy

app = FastAPI(
    title=f"{settings.PROJECT_NAME} - API Gateway",
    description="Main entry point for all LLM interactions.",
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
    return {"status": "gateway healthy"}

app.include_router(proxy.router, tags=["proxy"])
