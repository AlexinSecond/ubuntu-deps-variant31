@echo off
setlocal
cd /d "%~dp0.."
call run.bat --package A --repo examples/cycle.json --test-repo --max-depth 10 --ascii --output output/cycle.png
if errorlevel 1 exit /b 1
call run.bat --package A --repo examples/tree.json --test-repo --max-depth 1 --ascii --output output/depth1.png
if errorlevel 1 exit /b 1
call run.bat --package A --repo examples/tree.json --test-repo --exclude B --ascii --output output/filtered.png
if errorlevel 1 exit /b 1
call run.bat --package A --repo examples/diamond.json --test-repo --max-depth 3 --ascii --output output/diamond.png
exit /b %errorlevel%
