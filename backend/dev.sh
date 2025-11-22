#!/bin/bash

# Run FastAPI with hot reloading using uv
uv run uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
