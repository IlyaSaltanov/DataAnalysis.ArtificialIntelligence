@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
echo Jupyter откроется в браузере. Не закрывайте это окно, пока работаете.
uv run jupyter lab --notebook-dir=notebooks
pause
