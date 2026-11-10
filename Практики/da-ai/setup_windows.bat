@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Установка среды для практик "Анализ данных и ИИ" ===
echo.

where uv >nul 2>nul
if errorlevel 1 (
    echo [1/3] Устанавливаю uv в папку пользователя, права администратора не нужны...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
)
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where uv >nul 2>nul
if errorlevel 1 goto fail_uv

echo [2/3] Скачиваю Python 3.12 и библиотеки (первый раз 2-5 минут)...
uv sync
if errorlevel 1 goto fail_sync

echo [3/3] Проверяю среду...
uv run python check_env.py
if errorlevel 1 goto fail_check

echo.
echo Готово. Для запуска Jupyter дважды щёлкните start_jupyter.bat
pause
exit /b 0

:fail_uv
echo ОШИБКА: uv не установился. Скорее всего, нет доступа к astral.sh. Позовите преподавателя.
pause
exit /b 1
:fail_sync
echo ОШИБКА при загрузке библиотек. Проверьте интернет и запустите скрипт ещё раз.
pause
exit /b 1
:fail_check
echo Проверка не прошла. Покажите экран преподавателю.
pause
exit /b 1
