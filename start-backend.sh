#!/bin/bash

echo "More Insight Engine - Iniciando Backend"
echo "=========================================="

# Navigate to project root
cd "$(dirname "$0")"

# Start FastAPI server usando el Python del venv explícitamente
echo "📡 Iniciando servidor FastAPI en http://localhost:8000"
echo "⚠️  Nota: La primera vez puede tardar varios minutos descargando modelos"
echo ""

cd backend
../venv/bin/python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
