# LLMHub 🚀

> A production-grade, enterprise AI platform to deploy, manage, serve, route, monitor, and scale multiple Large Language Models.

## ❓ The Problem

Modern applications integrate directly with various LLM providers like OpenAI, Gemini, Claude, or local Ollama instances. As organizations adopt multiple AI providers, this creates:

*   **Duplicated Integrations:** Every application team implements custom client wrappers, retry logic, and error handling.
*   **Scattered API Keys:** Secrets are distributed across numerous environments and codebases, increasing security risks.
*   **Poor Monitoring:** Lack of centralized observability, logging, cost tracking, and request auditing.
*   **High Operational Costs:** No centralized caching (leading to redundant queries) or failover mechanism to fallback to cheaper providers/models.

## 💡 The Solution: Centralized AI Gateway

**LLMHub** solves these challenges by introducing a centralized, production-grade AI Gateway. 

Instead of applications calling providers directly, they communicate with LLMHub via a standardized API. LLMHub handles authentication, routing, caching, rate limiting, and analytics in a robust, microservices-based control plane.

```text
  Before LLMHub (Direct Integration Chaos)        After LLMHub (Centralized AI Gateway)

   ┌─────────┐       ┌─────────┐                   ┌─────────┐
   │  App A  ├──────>│ OpenAI  │                   │  App A  ├───┐
   └─────────┘       └─────────┘                   └─────────┘   │   ┌──────────────┐      ┌─────────┐
   ┌─────────┐       ┌─────────┐                   ┌─────────┐   ├──>│    LLMHub    ├─────>│ OpenAI  │
   │  App B  ├──────>│ Gemini  │                   │  App B  ├───┤   │  (AI Gateway)│      ├─────────┤
   └─────────┘       └─────────┘                   └─────────┘   │   └──────────────┘      │ Gemini  │
   ┌─────────┐       ┌─────────┐                   ┌─────────┐   │                         ├─────────┤
   │  App C  ├──────>│ Ollama  │                   │  App C  ├───┘                         │ Ollama  │
   └─────────┘       └─────────┘                   └─────────┘                             └─────────┘
```

## 🆚 Why not call OpenAI directly?

| Without LLMHub | With LLMHub |
| :--- | :--- |
| Every app stores provider API keys | Only LLMHub stores provider API keys |
| Provider-specific integrations | Single unified API |
| Switching providers requires app changes | Change routing rules only |
| No centralized analytics | Unified logging and dashboards |
| Separate rate limiting | Centralized rate limiting |

## 🌟 Features

* **Provider Agnostic:** Supports OpenAI, Anthropic, Gemini, Groq, Ollama, vLLM, and more via a unified interface.
* **Microservices Architecture:** Independently scalable Gateway, Auth, Router, and Analytics services.
* **Enterprise Security:** Built-in JWT authentication, API Key management, and rate limiting.
* **Smart Routing:** Seamlessly fallback and route traffic between local and cloud providers.
* **High Performance:** Designed for scale with asynchronous Python (FastAPI).

## 🏗️ Architecture

```text
                    Applications
                         │
                         ▼
                ┌─────────────────┐
                │     LLMHub      │
                ├─────────────────┤
                │ Authentication  │
                │ API Keys        │
                │ Rate Limiting   │
                │ Request Logging │
                │ Analytics       │
                │ Caching         │
                │ Model Routing   │
                │ Health Checks   │
                └─────────────────┘
                         │
   ┌───────┬────────┬────┴──┬────────┬───────┬───────┬────────┬───────┬────────┐
   ▼       ▼        ▼       ▼        ▼       ▼       ▼        ▼       ▼        ▼
 OpenAI  Gemini   Claude  Mistral  Cohere   Groq   Ollama   Azure  Bedrock  Together
```

LLMHub is organized into several specialized microservices and foundational layers:

* **`backend/gateway/`** - The primary entry point. Validates API keys and routes incoming requests.
* **`backend/auth-service/`** - Manages users, JWTs, and API Key lifecycle.
* **`backend/model-router/`** - The core engine that translates standard requests into provider-specific API calls.
* **`backend/shared/`** - The shared Python core containing database models and security utilities.
* **`frontend/`** - A sleek React application for managing keys, monitoring usage, and testing prompts.

## 🔌 API Example

LLMHub exposes a centralized AI Gateway endpoint. Application developers only need to point their client to the Gateway.

### Request

```http
POST /api/v1/chat
Authorization: Bearer llmhub_sk_xxxxx
Content-Type: application/json

{
  "profile": "invoice-extractor",
  "messages": [
    {
      "role": "user",
      "content": "Extract invoice details."
    }
  ]
}
```

### Response

```json
{
  "provider": "Gemini",
  "model": "gemini-2.5-flash",
  "latency": 420,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here are the extracted details from the invoice..."
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 📦 Client SDKs

We provide lightweight SDKs for seamless client-side integration.

### Python SDK

#### Installation
```bash
pip install ./sdk/python
```

#### Usage
```python
from llmhub import Client

client = Client(api_key="llmhub_sk_xxxxx", base_url="http://localhost:8000")

response = client.chat(
    profile="rag-chat",
    messages=[
        {"role": "user", "content": "How does LLMHub route models?"}
    ]
)

print(response["choices"][0]["message"]["content"])
```

### JavaScript SDK

#### Installation
```bash
npm install ./sdk/javascript
```

#### Usage
```javascript
const { Client } = require('llmhub-sdk');

const client = new Client({
  apiKey: 'llmhub_sk_xxxxx',
  baseUrl: 'http://localhost:8000'
});

async function run() {
  const response = await client.chat({
    profile: 'rag-chat',
    messages: [
      { role: 'user', content: 'Explain LLMHub routing.' }
    ]
  });

  console.log(response.choices[0].message.content);
}

run();
```

## 🚀 Quick Start (Development)

LLMHub uses a Docker-first approach for easy local development.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/LLM-Hub.git
   cd LLM-Hub
   ```

2. **Start the infrastructure (PostgreSQL, Redis):**
   ```bash
   docker-compose up -d
   ```

3. **Run the services locally:**
   ```bash
   # Make sure you are in the python virtual environment
   export PYTHONPATH=backend
   uvicorn backend.auth-service.app.main:app --reload
   ```

## 🗺️ Roadmap

- ✅ **Authentication** - JWT-based auth and service token validations.
- ✅ **API Keys** - Generate and manage client keys.
- ✅ **Gateway** - Async reverse proxy routing layer.
- ✅ **Provider Routing** - Automatic adapters for OpenAI, Claude, Gemini, etc.
- 🚧 **Analytics** - Centralized prompt/response logging and usage graphs.
- 🚧 **Cost Tracking** - Dynamic tracking of tokens and provider bills.
- 🚧 **Streaming** - Real-time Server-Sent Events (SSE) token streaming.
- ⬜ **Kubernetes** - Helm charts and multi-pod auto-scaling configurations.
- ⬜ **RBAC** - Advanced user role access control.
- ⬜ **Multi-tenancy** - Isolated environments for different teams/organizations.

## 🔮 Future Features

- **Semantic caching** - Check Redis for semantically identical requests using embeddings to reduce duplicate API costs.
- **Cost-aware routing** - Dynamically choose the cheapest equivalent model based on load and latency requirements.
- **Automatic failover** - Gracefully fallback to alternative providers (e.g., Anthropic to OpenAI) when error rates spike.
- **Prompt templates** - Version-control prompts directly on LLMHub and reference them via standard IDs.
- **Streaming responses** - Native Server-Sent Events (SSE) translation across all providers.
- **Model benchmarking** - Automatically benchmark response latencies, TTFT (Time To First Token), and throughput.
- **Multi-region deployment** - Geographically distributed routing to reduce latency.
- **Team workspaces** - Collaborative prompt playgrounds and key sharing.
- **Webhooks** - Receive real-time alerts for errors, anomalies, and quota limits.
- **Usage quotas** - Enforce soft/hard limits on usage/cost for specific API Keys and teams.
