import os
import time
import uuid
import json
import httpx
from typing import AsyncGenerator
from fastapi import HTTPException
from .base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse, ChatMessage, Choice, Usage

COHERE_API_URL = "https://api.cohere.ai/v1/chat"

class CohereProvider(BaseProvider):
    
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            import logging
            logging.warning("COHERE_API_KEY environment variable not set. API calls will fail.")
            
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _map_messages(self, messages):
        # Cohere expects: chat_history=[{"role": "USER"|"CHATBOT", "message": "..."}] and message="..."
        # System prompt is "preamble"
        chat_history = []
        preamble = ""
        current_message = ""
        
        for m in messages:
            if m.role == "system":
                preamble += m.content + "\n"
            elif m.role == "user":
                if current_message:
                    chat_history.append({"role": "USER", "message": current_message})
                current_message = m.content
            elif m.role == "assistant":
                if current_message:
                    chat_history.append({"role": "USER", "message": current_message})
                    current_message = ""
                chat_history.append({"role": "CHATBOT", "message": m.content})
                
        return chat_history, current_message, preamble.strip()

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        chat_history, message, preamble = self._map_messages(request.messages)
        
        payload = {
            "model": request.model,
            "message": message,
            "chat_history": chat_history,
            "temperature": request.temperature,
            "p": request.top_p,
        }
        if preamble:
            payload["preamble"] = preamble
            
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(COHERE_API_URL, headers=self._get_headers(), json=payload)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise HTTPException(status_code=502, detail=f"Error connecting to Cohere: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Cohere error: {e.response.text}")
                
        data = response.json()
        
        choice = Choice(
            index=0,
            message=ChatMessage(role="assistant", content=data.get("text", "")),
            finish_reason="stop"
        )
        
        usage_data = data.get("meta", {}).get("tokens", {})
        
        return ChatCompletionResponse(
            id=data.get("generation_id", f"chatcmpl-{uuid.uuid4().hex}"),
            created=int(time.time()),
            model=request.model,
            choices=[choice],
            usage=Usage(
                prompt_tokens=usage_data.get("input_tokens", 0),
                completion_tokens=usage_data.get("output_tokens", 0),
                total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0)
            )
        )
        
    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        yield "data: [COHERE_STREAMING_NOT_FULLY_IMPLEMENTED]\n\n"
        yield "data: [DONE]\n\n"
