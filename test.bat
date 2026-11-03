@echo off
setlocal
cd /d "%~dp0"
if defined PYTHON_EXE (
  "%PYTHON_EXE%" -m unittest discover -s tests -v
) else (
  py -3 -m unittest discover -s tests -v
)
exit /b %errorlevel%
