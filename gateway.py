import os
import time
import sqlite3
import httpx
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "gateway.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            provider TEXT,
            model TEXT,
            latency_ms INTEGER,
            status TEXT,
            key_snippet TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def log_request(provider: str, model: str, latency_ms: int, status: str, key_snippet: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO request_logs (timestamp, provider, model, latency_ms, status, key_snippet)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (time.strftime("%Y-%m-%d %H:%M:%S"), provider, model, latency_ms, status, key_snippet))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error writing to DB: {e}")

def get_recent_logs(limit: int = 50) -> List[Dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, provider, model, latency_ms, status, key_snippet
            FROM request_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "timestamp": r[0],
                "provider": r[1],
                "model": r[2],
                "latency_ms": r[3],
                "status": r[4],
                "key_snippet": r[5]
            }
            for r in rows
        ]
    except Exception as e:
        print(f"Error reading DB: {e}")
        return []

async def route_to_openai(model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return {"error": "OPENAI_API_KEY environment variable is not set."}
        
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": temperature},
                timeout=30.0
            )
            return resp.json()
        except Exception as e:
            return {"error": f"OpenAI request failed: {str(e)}"}

async def route_to_gemini(model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return {"error": "GEMINI_API_KEY environment variable is not set."}

    contents = []
    for m in messages:
        role = "user" if m.get("role") == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m.get("content", "")}]})

    async with httpx.AsyncClient() as client:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": contents,
                "generationConfig": {"temperature": temperature}
            }
            resp = await client.post(url, json=payload, timeout=30.0)
            data = resp.json()

            if "candidates" in data and data["candidates"]:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "provider": "Gemini",
                    "model": model,
                    "choices": [{"message": {"role": "assistant", "content": text}}]
                }
            elif "error" in data:
                return {"error": data["error"].get("message", "Gemini API error")}
            return data
        except Exception as e:
            return {"error": f"Gemini request failed: {str(e)}"}

async def route_to_claude(model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY environment variable is not set."}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": temperature
                },
                timeout=30.0
            )
            data = resp.json()
            if "content" in data and len(data["content"]) > 0:
                text = data["content"][0]["text"]
                return {
                    "provider": "Anthropic",
                    "model": model,
                    "choices": [{"message": {"role": "assistant", "content": text}}]
                }
            elif "error" in data:
                return {"error": data["error"].get("message", "Anthropic API error")}
            return data
        except Exception as e:
            return {"error": f"Anthropic request failed: {str(e)}"}

async def route_to_groq(model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return {"error": "GROQ_API_KEY environment variable is not set."}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages, "temperature": temperature},
                timeout=30.0
            )
            return resp.json()
        except Exception as e:
            return {"error": f"Groq request failed: {str(e)}"}

async def process_request(model: str, messages: List[Dict], temperature: float = 0.7, api_key: str = "") -> Dict:
    start_time = time.time()
    
    model_lower = model.lower()
    if "claude" in model_lower:
        provider = "Anthropic"
        response = await route_to_claude(model, messages, temperature)
    elif "gemini" in model_lower:
        provider = "Gemini"
        response = await route_to_gemini(model, messages, temperature)
    elif "llama" in model_lower or "mixtral" in model_lower or "groq" in model_lower:
        provider = "Groq"
        response = await route_to_groq(model, messages, temperature)
    else:
        provider = "OpenAI"
        response = await route_to_openai(model, messages, temperature)

    latency = int((time.time() - start_time) * 1000)
    status = "Success" if "error" not in response else "Failed"
    key_snippet = api_key[-4:] if api_key else "Default"

    log_request(provider, model, latency, status, key_snippet)
    
    return response
