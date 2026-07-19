from abc import ABC
from typing import AsyncGenerator
import os, json, httpx
from model_router.providers.base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

class AzureProvider(BaseProvider):
    """Adapter for Azure OpenAI service.
    Expects the following environment variables:
      * AZURE_OPENAI_ENDPOINT – e.g. https://{your-resource}.openai.azure.com/
      * AZURE_OPENAI_API_KEY – the key for the resource
      * AZURE_OPENAI_DEPLOYMENT – name of the model deployment (e.g., gpt-4o-deployment)
    The model name in the request is mapped to the deployment name.
    """

    def _get_headers(self) -> dict:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("AZURE_OPENAI_API_KEY not set in environment")
        return {"api-key": api_key, "Content-Type": "application/json"}

    def _get_base_url(self) -> str:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not endpoint:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT not set in environment")
        # Ensure trailing slash
        return endpoint.rstrip("/")

    def _deployment_for_model(self, model: str) -> str:
        # Allow admin to map a model name to a deployment via env var, fallback to model itself.
        return os.getenv(f"AZURE_OPENAI_DEPLOYMENT_{model.upper()}", model)

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        payload = request.model_dump(exclude_none=True)
        deployment = self._deployment_for_model(request.model)
        url = f"{self._get_base_url()}/openai/deployments/{deployment}/chat/completions?api-version=2023-05-15"
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            data = resp.json()
            return ChatCompletionResponse(**data)

    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        payload = request.model_dump(exclude_none=True)
        payload["stream"] = True
        deployment = self._deployment_for_model(request.model)
        url = f"{self._get_base_url()}/openai/deployments/{deployment}/chat/completions?api-version=2023-05-15"
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
