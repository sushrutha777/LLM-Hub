from abc import ABC
from typing import AsyncGenerator
import os, json, httpx
from model_router.providers.base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

class TogetherProvider(BaseProvider):
    """Adapter for Together AI models.
    Expects TOGETHER_API_KEY in environment.
    Calls the generic Together endpoint.
    """

    def _get_headers(self) -> dict:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise RuntimeError("TOGETHER_API_KEY not set in environment")
        return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        payload = request.model_dump(exclude_none=True)
        url = "https://api.together.xyz/v1/chat/completions"
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            data = resp.json()
            return ChatCompletionResponse(**data)

    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        payload = request.model_dump(exclude_none=True)
        payload["stream"] = True
        url = "https://api.together.xyz/v1/chat/completions"
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", url, headers=self._get_headers(), json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            yield f"{line}\n"
            except Exception as e:
                error_payload = json.dumps({"error": str(e)})
                yield f"data: {error_payload}\n\n"
