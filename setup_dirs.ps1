$dirs = @(
    "docs/architecture", "docs/api", "docs/database", "docs/deployment", "docs/diagrams", "docs/screenshots",
    "frontend/public", "frontend/src/app", "frontend/src/assets", "frontend/src/components", "frontend/src/features",
    "frontend/src/hooks", "frontend/src/layouts", "frontend/src/pages", "frontend/src/routes", "frontend/src/services",
    "frontend/src/store", "frontend/src/styles", "frontend/src/types", "frontend/src/utils",
    "backend/gateway/app", "backend/gateway/middleware", "backend/gateway/routes", "backend/gateway/security", "backend/gateway/config", "backend/gateway/tests",
    "backend/auth-service/app", "backend/auth-service/models", "backend/auth-service/routes", "backend/auth-service/services", "backend/auth-service/schemas", "backend/auth-service/utils", "backend/auth-service/tests",
    "backend/model-router/app", "backend/model-router/providers", "backend/model-router/router", "backend/model-router/services", "backend/model-router/tests",
    "backend/control-plane/app", "backend/control-plane/deployments", "backend/control-plane/models", "backend/control-plane/monitoring", "backend/control-plane/scheduler", "backend/control-plane/tests",
    "backend/analytics-service/app", "backend/analytics-service/metrics", "backend/analytics-service/reports", "backend/analytics-service/tests",
    "backend/notification-service/app", "backend/notification-service/email", "backend/notification-service/websocket", "backend/notification-service/tests",
    "backend/shared/config", "backend/shared/database", "backend/shared/exceptions", "backend/shared/logging", "backend/shared/middleware", "backend/shared/security", "backend/shared/utils", "backend/shared/constants",
    "backend/tests",
    "llm/ollama/Modelfiles", "llm/ollama/scripts", "llm/ollama/config", "llm/vllm/configs", "llm/vllm/scripts", "llm/prompts",
    "database/migrations", "database/init", "database/backups",
    "cache/scripts",
    "monitoring/prometheus", "monitoring/grafana", "monitoring/dashboards",
    "nginx/ssl",
    "kubernetes/gateway", "kubernetes/auth", "kubernetes/router", "kubernetes/analytics", "kubernetes/redis", "kubernetes/postgres", "kubernetes/ingress", "kubernetes/secrets", "kubernetes/monitoring",
    "docker/gateway", "docker/auth", "docker/router", "docker/analytics", "docker/postgres", "docker/redis",
    "scripts",
    "sdk/python", "sdk/javascript",
    "examples/curl", "examples/python", "examples/javascript", "examples/postman",
    ".github/workflows"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
