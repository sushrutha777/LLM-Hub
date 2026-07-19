import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from core.auth import get_api_key
from shared.database.models import APIKey

router = APIRouter()

# In a real microservice mesh, these would be env vars like http://model-router:8000
ROUTER_URL = "http://127.0.0.1:8001" 

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def reverse_proxy(
    request: Request, 
    path: str,
    api_key: APIKey = Depends(get_api_key)
):
    url = f"{ROUTER_URL}/{path}"
    
    body = await request.body()
    headers = dict(request.headers)
    
    # Inject user identity for downstream services
    headers["X-User-ID"] = str(api_key.user_id)
    headers["X-API-Key-ID"] = str(api_key.id)
    headers.pop("host", None) 

    client = httpx.AsyncClient()
    proxy_req = client.build_request(
        request.method,
        url,
        headers=headers,
        content=body,
        params=request.query_params
    )
    
    proxy_resp = await client.send(proxy_req, stream=True)
    
    async def stream_generator():
        async for chunk in proxy_resp.aiter_raw():
            yield chunk
        await client.aclose()

    return StreamingResponse(
        stream_generator(),
        status_code=proxy_resp.status_code,
        headers=dict(proxy_resp.headers)
    )
