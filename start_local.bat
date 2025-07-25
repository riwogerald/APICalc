@echo off
echo Starting Advanced Precision Calculator...
echo.

:: Start Python API Server in background
echo [1/3] Starting Python API Server...
start "Python API" cmd /k "python api_server.py"

:: Wait a moment for server to start
timeout /t 3 /nobreak > nul

:: Start React development server
echo [2/3] Starting React Frontend...
start "React Frontend" cmd /k "npm run dev"

:: Open browser
echo [3/3] Opening browser...
timeout /t 5 /nobreak > nul
start http://localhost:3000

echo.
echo ✅ Both servers started successfully!
echo 🌐 Frontend: http://localhost:3000
echo 🔌 API Server: http://localhost:5000
echo.
echo Press any key to stop all servers...
pause > nul

:: Stop all background processes
taskkill /fi "WindowTitle eq Python API*" /t /f > nul 2>&1
taskkill /fi "WindowTitle eq React Frontend*" /t /f > nul 2>&1
echo Servers stopped.
