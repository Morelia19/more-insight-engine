from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.transcriber import AudioTranscriber
from src.analyzer import PedagogicalAnalyzer
import shutil
import os
import json

app = FastAPI()

# Permitir que React se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelos al iniciar (puede tardar un poco)
transcriber = AudioTranscriber()
analyzer = PedagogicalAnalyzer()

@app.post("/process_class")
async def process_class(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    
    try:
        # 1. Guardar Audio
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Transcribir (Whisper)
        transcript = transcriber.transcribe(temp_file)
        
        # 3. Analizar (DeepSeek)
        raw_analysis = analyzer.analyze_class(transcript)
        
        # Intento de limpiar el JSON (DeepSeek a veces es hablador)
        try:
            start = raw_analysis.find('{')
            end = raw_analysis.rfind('}') + 1
            json_analysis = json.loads(raw_analysis[start:end])
        except:
            json_analysis = {"raw": raw_analysis, "error": "Formato no estricto"}

        return {
            "status": "success",
            "transcript": transcript,
            "report": json_analysis
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)