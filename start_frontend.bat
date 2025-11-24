@echo off
echo Starting Subscription Manager Frontend...
cd frontend
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)
start cmd /k npm run dev
pause

