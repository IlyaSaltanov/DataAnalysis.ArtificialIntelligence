#!/usr/bin/env bash
# Установка среды: Ubuntu и macOS. Запуск:  bash setup_linux.sh
set -e
cd "$(dirname "$0")"
echo '=== Установка среды для практик «Анализ данных и ИИ» ==='

if ! command -v uv >/dev/null 2>&1; then
    echo '[1/3] Устанавливаю uv в домашнюю папку, sudo не нужен...'
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        wget -qO- https://astral.sh/uv/install.sh | sh
    fi
fi
export PATH="$HOME/.local/bin:$PATH"

echo '[2/3] Скачиваю Python 3.12 и библиотеки (первый раз 2-5 минут)...'
uv sync

echo '[3/3] Проверяю среду...'
uv run python check_env.py

echo
echo 'Готово. Запуск Jupyter:  bash start_jupyter.sh'
