# Architecture Overview

LLMHub follows a Microservices Architecture designed for scalability, maintainability, and community contribution.

## Core Components

1. **API Gateway:** The single entry point. Validates JWTs, applies rate limits, and routes traffic.
2. **Auth Service:** Manages users and API Keys.
3. **Model Router:** The heart of LLMHub. Abstractly routes requests to underlying LLM Providers via a Plugin interface.
4. **Shared Module:** Common database schemas, utility functions, and configurations used by all Python microservices.
5. **Control Plane / Analytics:** Manages deployments and gathers operational metrics.

## Design Patterns

- **Clean Architecture:** Domain logic is decoupled from infrastructure.
- **Strategy Pattern (Plugins):** The `BaseProvider` interface allows anyone to implement a new LLM provider without touching the core routing logic.
- **Open/Closed Principle:** The platform is open for extension (adding models/providers) but closed for modification.
