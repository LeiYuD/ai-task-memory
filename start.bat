@echo off
chcp 65001 >nul
title AI 任务助手一键启动

echo ===================================================
echo 🚀 正在启动后端服务 (FastAPI)...
echo ===================================================
:: 进入后端目录，并在新窗口启动服务
cd backend
start "AI任务助手后端" cmd /k "python -m uvicorn app.main:app --reload"

:: 退回到根目录
cd ..

echo.
echo ===================================================
echo 🌐 正在启动前端网页...
echo ===================================================
:: 等待2秒让后端启动，然后打开前端的绝对路径
timeout /t 2 >nul
start "" "%~dp0frontend\index.html"

echo.
echo ✅ 启动完成！请勿关闭后端黑窗口。
pause