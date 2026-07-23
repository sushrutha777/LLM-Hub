Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "        🚀 Starting LLMHub 🚀          " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`n[1/4] Starting infrastructure (Redis & PostgreSQL)..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "`n[2/4] Starting API Gateway on Port 8000..." -ForegroundColor Yellow
Start-Process "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", "Title 'LLMHub API Gateway'; cd backend; `$env:PYTHONPATH='.'; venv\Scripts\python -m uvicorn gateway.app.main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "`n[3/4] Starting Model Router on Port 8001..." -ForegroundColor Yellow
Start-Process "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", "Title 'LLMHub Model Router'; cd backend; `$env:PYTHONPATH='.'; venv\Scripts\python -m uvicorn model_router.app.main:app --host 0.0.0.0 --port 8001 --reload"

Write-Host "`n[4/4] Starting React Dashboard on Port 5173..." -ForegroundColor Yellow
Start-Process "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", "Title 'LLMHub Frontend'; cd frontend; npm run dev"

Write-Host "`n✅ All services have been launched in separate windows!" -ForegroundColor Green
Write-Host "➡️  Open your browser to: http://localhost:5173" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
