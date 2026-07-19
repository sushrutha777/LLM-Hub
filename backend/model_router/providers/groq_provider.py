import os
import json
import httpx
from typing import AsyncGenerator
from fastapi import HTTPException
from .base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class GroqProvider(BaseProvider):
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            import logging
            logging.warning("GROQ_API_KEY environment variable not set. API calls will fail.")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        payload = request.model_dump(exclude_none=True)
        payload["stream"] = False
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(GROQ_API_URL, headers=self._get_headers(), json=payload)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise HTTPException(status_code=502, detail=f"Error connecting to Groq: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Groq error: {e.response.text}")
                
        return ChatCompletionResponse.model_validate(response.json())
        
    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        payload = request.model_dump(exclude_none=True)
        payload["stream"] = True
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", GROQ_API_URL, headers=self._get_headers(), json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            yield f"{line}\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
