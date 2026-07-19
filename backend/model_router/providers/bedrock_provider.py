from abc import ABC
from typing import AsyncGenerator
import os, json, httpx
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from model_router.providers.base_provider import BaseProvider
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

class BedrockProvider(BaseProvider):
    """Adapter for Amazon Bedrock chat models.
    Requires the following environment variables:
      * BEDROCK_REGION – AWS region (e.g., us-east-1)
      * BEDROCK_ACCESS_KEY – AWS Access Key ID
      * BEDROCK_SECRET_KEY – AWS Secret Access Key
    The model name in the request should match a Bedrock model identifier,
    e.g., "anthropic.claude-v2" or "meta.llama2-13b".
    """

    def _client(self):
        region = os.getenv("BEDROCK_REGION")
        access_key = os.getenv("BEDROCK_ACCESS_KEY")
        secret_key = os.getenv("BEDROCK_SECRET_KEY")
        if not all([region, access_key, secret_key]):
            raise RuntimeError("Bedrock credentials not fully set in environment")
        return boto3.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        # Bedrock uses a different payload structure; we map the OpenAI style to Bedrock.
        payload = {
            "prompt": "".join([msg.content for msg in request.messages]),
            "max_tokens": request.max_tokens or 1024,
            "temperature": request.temperature or 0.7,
            "top_p": request.top_p or 1,
        }
        client = self._client()
        try:
            response = client.invoke_model(
                body=json.dumps(payload).encode('utf-8'),
                modelId=request.model,
                accept="application/json",
                contentType="application/json",
            )
            resp_body = json.loads(response.get('body').read())
            # Transform Bedrock response to OpenAI‑style ChatCompletionResponse – this is a simple stub.
            return ChatCompletionResponse(**resp_body)
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Bedrock invocation error: {e}")

    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        # Bedrock does not (yet) support streaming via the SDK; we provide a non‑streaming fallback.
        response = await self.generate(request)
        # Emit the full response as a single SSE message.
        yield f"data: {json.dumps(response.model_dump())}\n\n"
