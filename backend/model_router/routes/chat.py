import hashlib
import json
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse
from model_router.providers.ollama_provider import OllamaProvider
from model_router.providers.openai_provider import OpenAIProvider
from model_router.providers.gemini_provider import GeminiProvider
from model_router.providers.groq_provider import GroqProvider
from model_router.providers.cohere_provider import CohereProvider
from model_router.providers.anthropic_provider import AnthropicProvider
from model_router.providers.azure_provider import AzureProvider
from model_router.providers.mistral_provider import MistralProvider
from model_router.providers.bedrock_provider import BedrockProvider
from model_router.providers.together_provider import TogetherProvider
from shared.config.settings import settings

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_provider(model_name: str):
    """Route model names to the correct provider adapter.
    Gemini is the default/base provider when no other prefix matches."""
    if model_name.startswith("gpt"):
        return OpenAIProvider()
    elif model_name.startswith("claude"):
        return AnthropicProvider()
    elif model_name.startswith("mistral"):
        return MistralProvider()
    elif model_name.startswith("command"):
        return CohereProvider()
    elif model_name.startswith("azure"):
        return AzureProvider()
    elif model_name.startswith("bedrock"):
        return BedrockProvider()
    elif model_name.startswith("together"):
        return TogetherProvider()
    elif model_name in ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]:
        return GroqProvider()
    elif model_name.startswith("ollama"):
        return OllamaProvider()
    else:
        # Default / base provider is Gemini
        return GeminiProvider()


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
    
    # Keep track of original requested model name
    original_model = body.model
    
    # 0. Resolve AI Profile logical name if applicable
    model_name = body.model
    cache_key_profile = f"profile:{model_name}"
    resolved_model = None
    try:
        resolved_model = await redis_client.get(cache_key_profile)
    except Exception:
        pass

    if not resolved_model:
        # Check SQLite DB for active profile
        from shared.database.session import SessionLocal
        from shared.database.models import AIProfile
        db = SessionLocal()
        try:
            profile = db.query(AIProfile).filter(AIProfile.id == model_name, AIProfile.is_active == True).first()
            if profile:
                resolved_model = profile.model_id
                try:
                    await redis_client.setex(cache_key_profile, 3600, resolved_model)
                except Exception:
                    pass
        finally:
            db.close()

    if resolved_model:
        body.model = resolved_model
        
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
                parsed["model"] = original_model # Make sure cached responses also report original model
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
        
        # Restore the original model name in the response
        response.model = original_model
        
        # Cache the result in Redis for 1 hour (3600 seconds)
        try:
            await redis_client.setex(cache_key, 3600, response.model_dump_json())
        except Exception as e:
            pass
            
        return response
