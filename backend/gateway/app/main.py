from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
from gateway.core.logging import RequestLoggingMiddleware
from gateway.routes import proxy, admin, models, profiles

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

app.add_middleware(RequestLoggingMiddleware)

@app.get("/health")
def health_check():
    return {"status": "gateway healthy"}

app.include_router(admin.router, prefix="/v1/admin", tags=["admin"])
app.include_router(profiles.router, prefix="/v1/admin/profiles", tags=["profiles"])
app.include_router(models.router, prefix="/v1/models", tags=["models"])
app.include_router(proxy.router, tags=["proxy"])
