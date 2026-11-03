@echo off
setlocal
cd /d "%~dp0.."
if defined PYTHON_EXE (
  "%PYTHON_EXE%" scripts\demo_errors.py
) else (
  py -3 scripts\demo_errors.py
)
exit /b %errorlevel%
