import httpx
import time
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from gateway.core.auth import get_api_key, get_db
from shared.database.models import APIKey, AIProfile, LLMModel, Provider

router = APIRouter()

# In a real microservice mesh, these would be env vars like http://model-router:8000
ROUTER_URL = "http://127.0.0.1:8001" 

@router.post("/api/v1/chat")
async def api_v1_chat(
    request: Request,
    api_key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
        
    profile = body.get("profile")
    messages = body.get("messages")
    
    if not profile or not messages:
        raise HTTPException(status_code=400, detail="Missing required fields: 'profile' and 'messages'")
        
    # Check if the profile exists
    db_profile = db.query(AIProfile).filter(AIProfile.id == profile, AIProfile.is_active == True).first()
    
    resolved_model = profile
    resolved_provider = "Unknown"
    
    if db_profile:
        resolved_model = db_profile.model_id
        # Get provider name
        db_provider = db.query(Provider).filter(Provider.id == db_profile.provider_id).first()
        if db_provider:
            resolved_provider = db_provider.name
        else:
            # Map known provider IDs to nice names as fallback
            provider_map = {
                "google": "Gemini",
                "openai": "OpenAI",
                "anthropic": "Anthropic",
                "ollama": "Ollama",
                "groq": "Groq",
                "mistral": "Mistral",
                "cohere": "Cohere",
                "together": "Together",
                "azure": "Azure",
                "aws": "Bedrock"
            }
            resolved_provider = provider_map.get(db_profile.provider_id.lower(), db_profile.provider_id.capitalize())
    else:
        # Check if the profile represents a raw model name directly
        db_model = db.query(LLMModel).filter(LLMModel.id == profile, LLMModel.is_active == True).first()
        if db_model:
            db_provider = db.query(Provider).filter(Provider.id == db_model.provider_id).first()
            if db_provider:
                resolved_provider = db_provider.name
            else:
                provider_map = {
                    "google": "Gemini",
                    "openai": "OpenAI",
                    "anthropic": "Anthropic",
                    "ollama": "Ollama"
                }
                resolved_provider = provider_map.get(db_model.provider_id.lower(), db_model.provider_id.capitalize())
        else:
            # Check prefix guess as ultimate fallback
            lower_profile = profile.lower()
            if lower_profile.startswith("gpt"):
                resolved_provider = "OpenAI"
            elif lower_profile.startswith("claude"):
                resolved_provider = "Anthropic"
            elif lower_profile.startswith("ollama"):
                resolved_provider = "Ollama"
            elif lower_profile.startswith("gemini") or "flash" in lower_profile or "pro" in lower_profile:
                resolved_provider = "Gemini"

    # Forward to downstream router service
    url = f"{ROUTER_URL}/v1/chat/completions"
    headers = {
        "X-User-ID": str(api_key.user_id),
        "X-API-Key-ID": str(api_key.id),
        "Content-Type": "application/json"
    }
    
    router_payload = {
        "model": profile, # This matches the incoming profile name which the router will resolve internally
        "messages": messages,
        "temperature": body.get("temperature", 0.7),
        "max_tokens": body.get("max_tokens"),
        "stream": False
    }
    
    start_time = time.time()
    
    async with httpx.AsyncClient() as client:
        try:
            router_resp = await client.post(
                url,
                json=router_payload,
                headers=headers,
                timeout=60.0
            )
            router_resp.raise_for_status()
            router_data = router_resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Inference router error: {str(e)}")
            
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Return formatted response to user's exact specification
    return {
        "provider": resolved_provider,
        "model": resolved_model,
        "latency": latency_ms,
        "choices": router_data.get("choices", [])
    }

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def reverse_proxy(
    request: Request, 
    path: str,
    api_key: APIKey = Depends(get_api_key)
):
    url = f"{ROUTER_URL}/{path}"
    
    body = await request.body()
    headers = dict(request.headers)
    
    # Inject user identity for downstream services
    headers["X-User-ID"] = str(api_key.user_id)
    headers["X-API-Key-ID"] = str(api_key.id)
    headers.pop("host", None) 

    client = httpx.AsyncClient()
    proxy_req = client.build_request(
        request.method,
        url,
        headers=headers,
        content=body,
        params=request.query_params
    )
    
    proxy_resp = await client.send(proxy_req, stream=True)
    
    async def stream_generator():
        async for chunk in proxy_resp.aiter_raw():
            yield chunk
        await client.aclose()

    return StreamingResponse(
        stream_generator(),
        status_code=proxy_resp.status_code,
        headers=dict(proxy_resp.headers)
    )

