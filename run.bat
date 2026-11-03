@echo off
setlocal
cd /d "%~dp0"
if defined PYTHON_EXE (
  "%PYTHON_EXE%" -m src %*
) else (
  py -3 -m src %*
)
exit /b %errorlevel%
