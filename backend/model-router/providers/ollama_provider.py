import time
import uuid
import json
import httpx
from typing import AsyncGenerator
from fastapi import HTTPException
from .base_provider import BaseProvider
from schemas.openai import ChatCompletionRequest, ChatCompletionResponse, ChatMessage, Choice, Usage

# In a real setup, this would be injected via settings
OLLAMA_API_URL = "http://127.0.0.1:11434"

class OllamaProvider(BaseProvider):
    
    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        url = f"{OLLAMA_API_URL}/api/chat"
        
        payload = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise HTTPException(status_code=502, detail=f"Error connecting to Ollama: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Ollama returned error: {e.response.text}")
                
        data = response.json()
        
        # Map back to OpenAI format
        choice = Choice(
            index=0,
            message=ChatMessage(role="assistant", content=data.get("message", {}).get("content", "")),
            finish_reason="stop" if data.get("done") else "unknown"
        )
        
        usage = Usage(
            prompt_tokens=data.get("prompt_eval_count", 0),
            completion_tokens=data.get("eval_count", 0),
            total_tokens=data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
        )
        
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            created=int(time.time()),
            model=request.model,
            choices=[choice],
            usage=usage
        )
        
    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        url = f"{OLLAMA_API_URL}/api/chat"
        payload = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": True,
            "options": {
                "temperature": request.temperature,
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                async with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            
                            # OpenAI chunk format
                            chunk = {
                                "id": f"chatcmpl-{uuid.uuid4().hex}",
                                "object": "chat.completion.chunk",
                                "created": int(time.time()),
                                "model": request.model,
                                "choices": [
                                    {
                                        "index": 0,
                                        "delta": {"content": data.get("message", {}).get("content", "")},
                                        "finish_reason": "stop" if data.get("done") else None
                                    }
                                ]
                            }
                            yield f"data: {json.dumps(chunk)}\n\n"
                            
                        except json.JSONDecodeError:
                            continue
                    yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
