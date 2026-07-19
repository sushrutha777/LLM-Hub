# LLMHub 🚀

## A production-grade, enterprise AI platform to deploy, manage, serve, route, monitor, and scale multiple Large Language Models.

LLMHub is a robust, microservices-based API Gateway and Model Router that standardizes how internal applications interact with Large Language Models. Instead of applications calling OpenAI, Anthropic, or local models directly, they communicate with LLMHub, which handles authentication, routing, caching, and rate limiting.

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
   ┌───────┬────────┬───────┬────────┬───┴───┬───────┬────────┬───────┬────────┐
   ▼       ▼        ▼       ▼        ▼       ▼       ▼        ▼       ▼        ▼
 OpenAI  Gemini   Claude  Mistral  Cohere   Groq   Ollama   Azure  Bedrock  Together
```

LLMHub is organized into several specialized microservices and foundational layers:

* **`backend/gateway/`** - The primary entry point. Validates API keys and routes incoming requests.
* **`backend/auth-service/`** - Manages users, JWTs, and API Key lifecycle.
* **`backend/model-router/`** - The core engine that translates standard requests into provider-specific API calls.
* **`backend/shared/`** - The shared Python core containing database models and security utilities.
* **`frontend/`** - A sleek React application for managing keys, monitoring usage, and testing prompts.

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

- [x] Scaffold Microservices Architecture
- [ ] Phase 1: Authentication & Basic Routing
- [ ] Phase 2: Multi-Model Support & Redis Caching
- [ ] Phase 3: Admin Control Plane & Monitoring
- [ ] Phase 4: Kubernetes Deployment Manifests
- [ ] Phase 5: Enterprise RBAC & Multi-Tenant Support
