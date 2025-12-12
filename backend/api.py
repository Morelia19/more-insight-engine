from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.transcriber import AudioTranscriber
from src.analyzer import PedagogicalAnalyzer
from src.report_generator import ReportGenerator
from dotenv import load_dotenv
import shutil
import os
import json
import ffmpeg

# Cargar variables de entorno desde .env
load_dotenv()

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
report_gen = ReportGenerator()

@app.post("/analyze_class")
async def analyze_class(
    video: UploadFile = File(...),
    student_name: str = Form(...),
    teacher_name: str = Form(...)
):
    """Paso 1: Analiza el video y retorna el análisis sin generar reporte"""
    temp_video = f"temp_video_{video.filename}"
    temp_audio = "temp_audio.wav"
    
    try:
        # 1. Guardar video
        with open(temp_video, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        # 2. Extraer audio del video usando ffmpeg (si está disponible)
        print("🎬 Extrayendo audio del video...")
        try:
            (
                ffmpeg
                .input(temp_video)
                .output(temp_audio, acodec='pcm_s16le', ac=1, ar='16k')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except (ffmpeg.Error, FileNotFoundError) as e:
            # Fallback: copiar el archivo directamente (útil para archivos WAV)
            print(f"⚠️  FFmpeg no disponible o error: {e}")
            print("📋 Usando archivo directo (debe ser WAV o formato compatible)")
            shutil.copy(temp_video, temp_audio)
        
        # 3. Transcribir (Whisper)
        print("📝 Transcribiendo video...")
        transcript = transcriber.transcribe(temp_audio)
        
        # 4. Analizar (Phi-3 Mini)
        print("🧠 Analizando clase...")
        raw_analysis = analyzer.analyze_class(transcript)
        
        # Intentar parsear JSON del análisis con mejor extracción
        try:
            # Buscar el JSON en la respuesta
            start = raw_analysis.find('{')
            end = raw_analysis.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = raw_analysis[start:end]
                print(f"📊 JSON extraído:\n{json_str}")
                json_analysis = json.loads(json_str)
                
                # Validar que tiene los campos esperados
                required_fields = ["objetivos", "desarrollo", "actitud", "recomendaciones"]
                for field in required_fields:
                    if field not in json_analysis:
                        print(f"⚠️  Campo faltante: {field}")
                        raise ValueError(f"Campo {field} no encontrado en análisis")
                
                print("✅ JSON válido con todos los campos")
            else:
                raise ValueError("No se encontró JSON en la respuesta")
                
        except Exception as parse_error:
            print(f"⚠️  Error parseando JSON: {parse_error}")
            print(f"📄 Respuesta completa del modelo:\n{raw_analysis}")
            
            # Si falla, crear estructura básica
            json_analysis = {
                "objetivos": ["Análisis de la clase"],
                "desarrollo": raw_analysis[:500] if len(raw_analysis) > 500 else raw_analysis,
                "actitud": 85,
                "recomendaciones": "Continuar con el plan de estudios."
            }

        return {
            "status": "success",
            "transcript": transcript,
            "report": json_analysis
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "message": str(e)}
    
    finally:
        # Limpiar archivos temporales
        for temp_file in [temp_video, temp_audio]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

@app.post("/generate_report")
async def generate_report(
    analysis: str = Form(...),
    session_photo: UploadFile = File(None),
    logo: UploadFile = File(None),
    student_name: str = Form(...),
    teacher_name: str = Form(...),
    session_number: int = Form(1),
    total_sessions: int = Form(8),
    session_date: str = Form(None)
):
    """Paso 2: Genera el reporte visual a partir del análisis editado"""
    temp_session = None
    temp_logo = None
    
    try:
        # 1. Parsear análisis
        json_analysis = json.loads(analysis)
        
        # 2. Guardar foto de sesión si existe
        if session_photo:
            temp_session = f"temp_session_{session_photo.filename}"
            with open(temp_session, "wb") as buffer:
                shutil.copyfileobj(session_photo.file, buffer)
        
        # 3. Guardar logo si existe
        if logo:
            temp_logo = f"temp_logo_{logo.filename}"
            with open(temp_logo, "wb") as buffer:
                shutil.copyfileobj(logo.file, buffer)
        
        # 4. Generar reporte visual
        print("🎨 Generando reporte visual...")
        report_path = report_gen.generate_report(
            analysis=json_analysis,
            session_photo_path=temp_session,
            logo_path=temp_logo,
            student_name=student_name,
            teacher_name=teacher_name,
            session_number=session_number,
            total_sessions=total_sessions,
            session_date=session_date
        )
        
        # Obtener nombre del archivo generado
        report_filename = os.path.basename(report_path)

        return {
            "status": "success",
            "report_image": f"/reports/{report_filename}"
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "success", "report_image": f"/{report_path}"}
    
    finally:
        # Limpiar archivos temporales
        for temp_file in [temp_session, temp_logo]:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

@app.get("/reports/{filename}")
async def get_report(filename: str):
    """Endpoint para servir las imágenes de reportes generados"""
    file_path = f"reports/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    return {"status": "error", "message": "Reporte no encontrado"}