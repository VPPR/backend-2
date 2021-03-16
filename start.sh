#!/usr/bin/env bash

# shellcheck disable=SC1091

[[ -d "venv" ]] || python3.8 -m venv ./venv
source venv/bin/activate
pip install -U -r requirements.txt
uvicorn app.server:app --host=127.0.0.1 --port=8001