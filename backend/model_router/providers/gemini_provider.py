import os
import time
import uuid
import json
import httpx
from typing import AsyncGenerator
from fastapi import HTTPException
from .base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse, ChatMessage, Choice, Usage

class GeminiProvider(BaseProvider):
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            import logging
            logging.warning("GEMINI_API_KEY environment variable not set. API calls will fail.")
            
    def _map_messages(self, messages):
        gemini_messages = []
        system_instruction = None
        
        for m in messages:
            if m.role == "system":
                system_instruction = {"parts": [{"text": m.content}]}
            elif m.role == "user":
                gemini_messages.append({"role": "user", "parts": [{"text": m.content}]})
            elif m.role == "assistant":
                gemini_messages.append({"role": "model", "parts": [{"text": m.content}]})
                
        return gemini_messages, system_instruction

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{request.model}:generateContent?key={self.api_key}"
        
        contents, system_instruction = self._map_messages(request.messages)
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "topP": request.top_p,
            }
        }
        if system_instruction:
            payload["systemInstruction"] = system_instruction
            
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise HTTPException(status_code=502, detail=f"Error connecting to Gemini: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Gemini error: {e.response.text}")
                
        data = response.json()
        
        text = ""
        if "candidates" in data and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                text = candidate["content"]["parts"][0].get("text", "")
                
        choice = Choice(
            index=0,
            message=ChatMessage(role="assistant", content=text),
            finish_reason="stop"
        )
        
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            created=int(time.time()),
            model=request.model,
            choices=[choice],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
        )
        
    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        # Minimal stub for streaming logic mapping SSE to Gemini
        yield "data: [GEMINI_STREAMING_NOT_FULLY_IMPLEMENTED]\n\n"
        yield "data: [DONE]\n\n"
