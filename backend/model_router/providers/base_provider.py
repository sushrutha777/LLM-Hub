from abc import ABC, abstractmethod
from typing import AsyncGenerator
from model_router.schemas.openai import ChatCompletionRequest, ChatCompletionResponse

class BaseProvider(ABC):
    
    @abstractmethod
    async def generate(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Generate a standard chat completion response."""
        pass
        
    @abstractmethod
    async def stream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        """Generate a streaming response formatted as SSE (Server-Sent Events)."""
        pass
