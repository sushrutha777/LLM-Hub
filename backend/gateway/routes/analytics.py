from fastapi import APIRouter

router = APIRouter()

# Mock data based on the dashboard
mock_metrics = [
    { 
        "title": 'Total Requests', 
        "subtitle": 'API calls processed through the gateway',
        "value": '12,567', 
        "trend": '+14%', 
        "positive": True 
    },
    { 
        "title": 'Avg Latency', 
        "subtitle": 'Mean response time across all providers',
        "value": '340 ms', 
        "trend": '-22ms', 
        "positive": True 
    },
    { 
        "title": 'Cache Hit Rate', 
        "subtitle": 'Percentage of requests served from Redis cache',
        "value": '71%', 
        "trend": '+5%', 
        "positive": True 
    },
    { 
        "title": 'Active Providers', 
        "subtitle": 'Providers with configured API keys',
        "value": '5 / 10', 
        "trend": '', 
        "positive": True 
    },
]

mock_models = [
    { "name": 'Gemini 1.5 Flash', "provider": 'Google', "usage": '38%', "color": '#6366f1' },
    { "name": 'GPT-4o', "provider": 'OpenAI', "usage": '26%', "color": '#10b981' },
    { "name": 'Claude 3.5 Sonnet', "provider": 'Anthropic', "usage": '18%', "color": '#f59e0b' },
    { "name": 'Mixtral 8x7B', "provider": 'Groq', "usage": '12%', "color": '#ef4444' },
    { "name": 'Command R', "provider": 'Cohere', "usage": '6%', "color": '#a855f7' },
]

mock_providers = [
    { "name": 'Google Gemini', "percentage": 38, "color": '#6366f1' },
    { "name": 'OpenAI', "percentage": 26, "color": '#10b981' },
    { "name": 'Anthropic', "percentage": 18, "color": '#f59e0b' },
    { "name": 'Groq', "percentage": 12, "color": '#ef4444' },
    { "name": 'Cohere', "percentage": 6, "color": '#a855f7' },
]

@router.get("/metrics")
def get_metrics():
    return mock_metrics

@router.get("/models")
def get_models():
    return mock_models

@router.get("/providers")
def get_providers():
    return mock_providers
