#!/bin/bash

echo "More Insight Engine - Iniciando Backend"
echo "=========================================="

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
echo "📡 Iniciando servidor FastAPI en http://localhost:8000"
echo "⚠️  Nota: La primera vez puede tardar varios minutos descargando modelos"
echo ""

cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
