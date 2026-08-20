@echo off
chcp 65001 >nul
title 沃土之环 - 本地开发启动
echo ============================================
echo   🌱 沃土之环 (TerraHalo) - 本地开发启动
echo ============================================
echo.
echo  [1/2] 启动 Flask 后端  (http://localhost:5000)
start "TerraHalo-Backend" cmd /k "cd /d %~dp0TerraHalo\Backend_folder && python app.py"
echo  [2/2] 启动网页端静态服务器  (http://localhost:8000)
start "TerraHalo-Web" cmd /k "cd /d %~dp0TerraHalo-Web && python -m http.server 8000"
echo.
echo  ✅ 完成后请用浏览器访问:  http://localhost:8000
echo.
echo  📋 测试账号:
echo      [农户/供应商] 绿色农场 / 123456
echo      [企业]        有机肥厂 / 123456
echo      [司机]        司机小李 / 123456
echo      [管理员]      admin    / admin123
echo.
pause
