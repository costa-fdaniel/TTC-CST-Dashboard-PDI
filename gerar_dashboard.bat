@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0gerar_dashboard.ps1"
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0gerar_dashboard.ps1" -InputPath "%~1"
)

pause
