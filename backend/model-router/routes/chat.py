from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from schemas.openai import ChatCompletionRequest, ChatCompletionResponse
from providers.ollama_provider import OllamaProvider

router = APIRouter()

# In a more advanced implementation, this would be a dynamic registry
def get_provider(model_name: str):
    # For Phase 1, we just route everything to Ollama
    return OllamaProvider()

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: Request,
    body: ChatCompletionRequest
):
    # Security contexts injected by the Gateway
    user_id = request.headers.get("X-User-ID")
    api_key_id = request.headers.get("X-API-Key-ID")
    
    # In Phase 2: Add Analytics/Usage tracking hooks here
    
    provider = get_provider(body.model)
    
    if body.stream:
        return StreamingResponse(
            provider.stream(body),
            media_type="text/event-stream"
        )
    else:
        return await provider.generate(body)
