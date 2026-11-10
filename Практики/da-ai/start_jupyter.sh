#!/usr/bin/env bash
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"
echo 'Jupyter откроется в браузере. Не закрывайте терминал, пока работаете.'
uv run jupyter lab --notebook-dir=notebooks
