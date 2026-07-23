import os
import sys
import subprocess
import httpx
from fastapi import FastAPI, Request, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import websockets
from gateway import process_request

app = FastAPI(title="LLMHub AI Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start Streamlit process using sys.executable on startup
@app.on_event("startup")
def start_streamlit():
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--server.headless=true",
        "--server.allowRunOnSave=false"
    ])

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer llmhub_sk_"):
        raise HTTPException(status_code=401, detail="Invalid or missing Gateway API key")
    
    api_key = authorization.split(" ")[1]
    messages_dict = [{"role": m.role, "content": m.content} for m in req.messages]
    
    res = await process_request(req.model, messages_dict, req.temperature, api_key)
    if "error" in res:
        raise HTTPException(status_code=500, detail=res["error"])
    return res

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "LLMHub AI Gateway"}

# WebSocket proxy for Streamlit interactive updates
@app.websocket("/_stcore/stream")
async def websocket_proxy(ws: WebSocket):
    await ws.accept()
    async with websockets.connect("ws://127.0.0.1:8501/_stcore/stream") as target_ws:
        async def forward_to_target():
            try:
                while True:
                    data = await ws.receive_bytes()
                    await target_ws.send(data)
            except Exception:
                pass

        async def forward_to_client():
            try:
                while True:
                    data = await target_ws.recv()
                    if isinstance(data, str):
                        await ws.send_text(data)
                    else:
                        await ws.send_bytes(data)
            except Exception:
                pass

        await asyncio.gather(forward_to_target(), forward_to_client(), return_exceptions=True)

# Proxy HTTP UI requests to Streamlit on 8501
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
async def proxy_to_streamlit(request: Request, path: str):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8501") as client:
        url = f"/{path}"
        if request.url.query:
            url += f"?{request.url.query}"
            
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                timeout=30.0
            )
            return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
        except Exception:
            return Response(content="LLMHub Gateway UI is initializing...", status_code=200)
