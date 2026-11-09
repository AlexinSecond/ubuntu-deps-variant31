@echo off
setlocal
cd /d "%~dp0.."
call run.bat --package bash --max-depth 2 --ascii --output output/bash.png
if errorlevel 1 exit /b 1
call run.bat --package grep --max-depth 2 --ascii --output output/grep.png
if errorlevel 1 exit /b 1
call run.bat --package sed --max-depth 2 --ascii --output output/sed.png
exit /b %errorlevel%
