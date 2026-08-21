@echo off
chcp 65001 >nul
title 沃土之环 - 一键启动（网页端主界面）
echo ============================================
echo   🌱 沃土之环 (TerraHalo) - 一键启动
echo ============================================
echo.
echo  🎯 网页端主界面：http://localhost:8000
echo.
echo  [1/2] 启动后端 API  (http://localhost:5000)
start "TerraHalo-Backend" cmd /k "cd /d %~dp0TerraHalo\Backend_folder && python app.py"
echo  [2/2] 启动网页端服务器  (http://localhost:8000)
start "TerraHalo-Web" cmd /k "cd /d %~dp0TerraHalo-Web && python -m http.server 8000"
echo.
echo  ⏳ 等待服务就绪，自动打开浏览器…
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000"
echo.
echo  📋 测试账号:
echo      [管理员]      admin    / admin123   → 管理总控室
echo      [企业]        有机肥厂 / 123456
echo      [供应商/农户] 绿色农场 / 123456
echo      [司机]        司机小李 / 123456
echo.
pause
