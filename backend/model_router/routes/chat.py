import hashlib
import json
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse
from model_router.providers.ollama_provider import OllamaProvider
from model_router.providers.openai_provider import OpenAIProvider
from model_router.providers.gemini_provider import GeminiProvider
from shared.config.settings import settings

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_provider(model_name: str):
    if model_name.startswith("gpt"):
        return OpenAIProvider()
    elif model_name.startswith("gemini"):
        return GeminiProvider()
    else:
        # Fallback to local models via Ollama
        return OllamaProvider()

def generate_cache_key(body: ChatCompletionRequest) -> str:
    # Hash the model, messages, and temp to form a unique cache key
    data_to_hash = {
        "model": body.model,
        "messages": [{"role": m.role, "content": m.content} for m in body.messages],
        "temperature": body.temperature
    }
    hash_str = json.dumps(data_to_hash, sort_keys=True).encode('utf-8')
    return f"cache:completion:{hashlib.md5(hash_str).hexdigest()}"

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: Request,
    body: ChatCompletionRequest
):
    user_id = request.headers.get("X-User-ID")
    api_key_id = request.headers.get("X-API-Key-ID")
    
    cache_key = generate_cache_key(body)
    
    # 1. Check Redis Cache for exact semantic match (Non-streaming only for phase 2)
    if not body.stream:
        try:
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                import logging
                logging.info(f"Cache HIT for {cache_key}")
                # Inject a meta flag indicating it was cached
                parsed = json.loads(cached_result)
                parsed["cached"] = True 
                return JSONResponse(content=parsed)
        except Exception as e:
            import logging
            logging.error(f"Redis cache error: {e}")
            
    # 2. Get dynamic provider
    provider = get_provider(body.model)
    
    # 3. Generate response
    if body.stream:
        return StreamingResponse(
            provider.stream(body),
            media_type="text/event-stream"
        )
    else:
        response = await provider.generate(body)
        
        # Cache the result in Redis for 1 hour (3600 seconds)
        try:
            await redis_client.setex(cache_key, 3600, response.model_dump_json())
        except Exception as e:
            pass
            
        return response
