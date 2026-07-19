from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
from routes import auth, keys

app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Auth Service",
    openapi_url=f"{settings.API_V1_STR}/auth/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(keys.router, prefix=f"{settings.API_V1_STR}/keys", tags=["keys"])

@app.get("/health")
def health_check():
    return {"status": "auth-service healthy"}
