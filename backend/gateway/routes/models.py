from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# Hardcoded catalog based on the top 10 industry providers list
MODEL_CATALOG = [
    {
        "id": "openai",
        "name": "OpenAI",
        "rank": 1,
        "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "best_for": "General AI, coding, agents",
        "free_tier": False,
        "status": "active"
    },
    {
        "id": "google",
        "name": "Google",
        "rank": 2,
        "models": ["gemini-1.5-pro", "gemini-1.5-flash"],
        "best_for": "Multimodal, RAG, long context",
        "free_tier": True,
        "status": "active"
    },
    {
        "id": "anthropic",
        "name": "Anthropic",
        "rank": 3,
        "models": ["claude-3-opus", "claude-3-5-sonnet", "claude-3-haiku"],
        "best_for": "Reasoning, coding, enterprise",
        "free_tier": False,
        "status": "planned"
    },
    {
        "id": "groq",
        "name": "Groq",
        "rank": 4,
        "models": ["llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
        "best_for": "Ultra-fast inference",
        "free_tier": True,
        "status": "active"
    },
    {
        "id": "cohere",
        "name": "Cohere",
        "rank": 5,
        "models": ["command-r", "command-r-plus"],
        "best_for": "Enterprise RAG, search",
        "free_tier": True,
        "status": "active"
    },
    {
        "id": "xai",
        "name": "xAI",
        "rank": 6,
        "models": ["grok-1.5"],
        "best_for": "Reasoning, coding",
        "free_tier": False,
        "status": "planned"
    },
    {
        "id": "mistral",
        "name": "Mistral AI",
        "rank": 7,
        "models": ["mistral-large", "ministral"],
        "best_for": "European AI, multilingual",
        "free_tier": False,
        "status": "planned"
    },
    {
        "id": "together",
        "name": "Together AI",
        "rank": 8,
        "models": ["llama-3", "deepseek-coder"],
        "best_for": "Open-source model hosting",
        "free_tier": True,
        "status": "planned"
    },
    {
        "id": "openrouter",
        "name": "OpenRouter",
        "rank": 9,
        "models": ["300+ models via single API"],
        "best_for": "One API for many providers",
        "free_tier": True,
        "status": "planned"
    },
    {
        "id": "fireworks",
        "name": "Fireworks AI",
        "rank": 10,
        "models": ["llama-3", "qwen"],
        "best_for": "High-performance inference",
        "free_tier": True,
        "status": "planned"
    }
]

@router.get("/")
async def list_models() -> Dict[str, Any]:
    """
    Returns the catalog of supported and planned models in LLMHub.
    This mimics the standard OpenAI /v1/models endpoint format but 
    returns our curated Top 10 list.
    """
    return {
        "object": "list",
        "data": MODEL_CATALOG
    }
