import httpx
from typing import List, Dict, Any, Optional

class LLMHubError(Exception):
    """Base exception for LLMHub SDK errors."""
    pass

class Client:
    """Client for interacting with the LLMHub API Gateway."""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        """
        Initialize the LLMHub client.
        
        Args:
            api_key: The API Key for authorization.
            base_url: The base URL of the LLMHub gateway (defaults to http://localhost:8000).
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, profile: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to the LLMHub Gateway.
        
        Args:
            profile: The active model profile (e.g. 'rag-chat', 'invoice-extractor').
            messages: A list of messages (e.g. [{'role': 'user', 'content': 'Hello'}])
            **kwargs: Additional parameters passed to the gateway (e.g. temperature, max_tokens)
            
        Returns:
            Dict containing the chat completion response.
        """
        url = f"{self.base_url}/api/v1/chat"
        payload = {
            "profile": profile,
            "messages": messages,
            **kwargs
        }
        
        with httpx.Client() as client:
            try:
                response = client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise LLMHubError(f"HTTP error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise LLMHubError(f"Request failed: {e}")
