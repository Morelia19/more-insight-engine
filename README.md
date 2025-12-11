# 🎓 More Insight Engine

**Auditoría Pedagógica Automatizada con IA**

Sistema de análisis de clases educativas que utiliza Whisper para transcripción de audio y DeepSeek V2 Lite para análisis pedagógico automatizado.

## 🌟 Características

- **Transcripción Automática**: Convierte audio de clases a texto usando Whisper de OpenAI
- **Análisis Pedagógico IA**: Evalúa calidad educativa usando DeepSeek V2 Lite
- **API REST**: Backend FastAPI para procesamiento
- **Interfaz Web**: Frontend React con UI moderna

## 📋 Requisitos Previos

- Python 3.10+
- Node.js 18+
- macOS con Apple Silicon (para MPS) o Linux/Windows con NVIDIA GPU

## 🚀 Instalación

### 1. Backend (Python)

```bash
cd more-insight-engine

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows

# Instalar dependencias
# IMPORTANTE: Usar --trusted-host si tienes problemas de SSL
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org torch torchvision torchaudio
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org transformers accelerate sentencepiece protobuf
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi uvicorn python-multipart
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org bitsandbytes
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org git+https://github.com/openai/whisper.git
```

### 2. Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install
```

## 🎮 Uso

### Iniciar Backend

```bash
cd more-insight-engine
source venv/bin/activate
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`

### Iniciar Frontend

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📝 Cómo Funciona

1. **Subir Audio**: El usuario carga un archivo de audio de una clase
2. **Transcripción**: Whisper convierte el audio a texto
3. **Análisis**: DeepSeek V2 Lite analiza la transcripción y genera un reporte pedagógico
4. **Resultados**: El sistema muestra la transcripción y el análisis en formato JSON

## ⚙️ Configuración

### Cambiar Modelo de Whisper

En `backend/src/transcriber.py`, cambia el parámetro `model_size`:

```python
transcriber = AudioTranscriber(model_size="medium")  # o "small", "base", "large"
```

Modelos disponibles:
- `tiny`: Más rápido, menos preciso
- `base`: Balanceado
- `small`: **Por defecto**, buena calidad
- `medium`: Mayor precisión
- `large`: Máxima precisión (requiere más RAM)

### Prompt Pedagógico

El prompt de análisis está en `backend/src/analyzer.py`. Puedes personalizarlo según tus necesidades educativas.

## ⚠️ Notas Importantes

### macOS (Apple Silicon)

- ✅ **MPS está habilitado** para aceleración GPU en Whisper
- ⚠️ **bitsandbytes tiene capacidades limitadas** en macOS (no soporta quantización 4-bit completamente)
- 🔧 **DeepSeek V2 Lite** puede tardar en cargar la primera vez (descarga ~15GB)

### Memoria RAM

- Whisper `small`: ~2GB RAM
- DeepSeek V2 Lite (4-bit): ~8-10GB RAM
- **Total recomendado**: 16GB RAM mínimo

## 🐛 Solución de Problemas

### Error de SSL con pip

Siempre usa los flags `--trusted-host`:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <paquete>
```

### DeepSeek No Funciona en macOS

Si bitsandbytes falla, considera:
- Usar `load_in_8bit` en lugar de `load_in_4bit`
- Usar un modelo más pequeño
- Ejecutar en CPU (más lento pero funcional)

### Whisper Usa CPU en lugar de GPU

Verifica que MPS esté disponible:

```python
import torch
print(f"MPS disponible: {torch.backends.mps.is_available()}")
```

## 📦 Estructura del Proyecto

```
more-insight-engine/
├── backend/
│   ├── api.py                  # FastAPI app principal
│   └── src/
│       ├── transcriber.py      # Módulo Whisper
│       └── analyzer.py         # Módulo DeepSeek
└── frontend/
    ├── src/
    │   ├── App.jsx            # Componente principal
    │   ├── main.jsx
    │   └── index.css          # Tailwind CSS
    └── package.json
```

## 🎯 Próximas Mejoras

- [ ] Soporte para múltiples archivos
- [ ] Interfaz para visualizar métricas pedagógicas
- [ ] Base de datos para histórico de análisis
- [ ] Exportación de reportes a PDF
- [ ] Autenticación de usuarios

## 📄 Licencia

Este proyecto es para uso académico en More Academy.

## 🤝 Contribuciones

Este es un proyecto de investigación. Para sugerencias, por favor contacta al autor.

---