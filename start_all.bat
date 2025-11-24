@echo off
echo Starting Subscription Manager...
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -m venv venv 2>nul && call venv\Scripts\activate && pip install -r requirements.txt >nul 2>&1 && python main.py"
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && if not exist node_modules (call npm install) && npm run dev"
echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause

