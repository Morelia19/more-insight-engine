#!/usr/bin/env python3
"""
Script de prueba para el More Insight Engine API
Crea un video de prueba y lo envía al servidor para analizar
"""
import requests
import json
import os
import sys
from pathlib import Path

# URL del servidor
API_URL = "http://localhost:8000"

def create_test_video():
    """Crea un video de prueba corto con audio sintético"""
    try:
        # Intentar crear un video de prueba usando ffmpeg
        import subprocess
        
        output_file = "test_video.mp4"
        
        # Generar un video de prueba de 5 segundos con un tono de audio
        # Esto crea un video negro con un tono de 440 Hz (nota La)
        cmd = [
            "ffmpeg", "-f", "lavfi", "-i", "color=c=black:s=640x480:d=5",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=5",
            "-shortest", "-y", output_file
        ]
        
        print("🎬 Creando video de prueba...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  No se pudo crear video sintético. Usando método alternativo...")
            return None
            
        print(f"✅ Video de prueba creado: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"⚠️  Error creando video: {e}")
        return None

def test_analyze_endpoint(video_path=None):
    """Prueba el endpoint /analyze_class"""
    
    if not video_path:
        print("⚠️  No hay video de prueba. ")
        print("Por favor, coloca un archivo de video (mp4, mov, etc.) en el directorio actual")
        print("y ejecútalo con: python test_api.py <nombre_del_video>")
        return
    
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"🧪 PROBANDO: /analyze_class")
    print(f"{'='*60}\n")
    
    # Datos de la sesión
    data = {
        "student_name": "María García",
        "teacher_name": "Juan Pérez"
    }
    
    # Archivo de video
    with open(video_path, "rb") as f:
        files = {"video": (os.path.basename(video_path), f, "video/mp4")}
        
        print(f"📤 Subiendo video: {video_path}")
        print(f"   Estudiante: {data['student_name']}")
        print(f"   Profesor: {data['teacher_name']}")
        print(f"\n⏳ Procesando (esto puede tardar varios minutos)...")
        print(f"   - Extrayendo audio del video...")
        print(f"   - Transcribiendo con Whisper...")
        print(f"   - Analizando con Phi-3 Mini...\n")
        
        try:
            response = requests.post(
                f"{API_URL}/analyze_class",
                data=data,
                files=files,
                timeout=600  # 10 minutos de timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n{'='*60}")
                print(f"✅ ANÁLISIS COMPLETADO")
                print(f"{'='*60}\n")
                
                # Mostrar transcripción
                print("📝 TRANSCRIPCIÓN:")
                print("-" * 60)
                transcript = result.get("transcript", "")
                if len(transcript) > 500:
                    print(f"{transcript[:500]}...\n[transcripción truncada, total: {len(transcript)} caracteres]")
                else:
                    print(transcript)
                
                # Mostrar análisis JSON
                print(f"\n🧠 ANÁLISIS PEDAGÓGICO (JSON):")
                print("-" * 60)
                report = result.get("report", {})
                print(json.dumps(report, indent=2, ensure_ascii=False))
                
                # Guardar resultado en archivo
                output_file = "test_result.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Resultado completo guardado en: {output_file}")
                
                print(f"\n{'='*60}")
                print("✅ PRUEBA EXITOSA")
                print(f"{'='*60}\n")
                
            else:
                print(f"❌ Error HTTP {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Timeout: El servidor tardó demasiado en responder")
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión: ¿Está el servidor corriendo en http://localhost:8000?")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    print(f"""
{'='*60}
🧪 More Insight Engine - Prueba de API
{'='*60}
    """)
    
    # Verificar si el servidor está corriendo
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        print("✅ Servidor detectado en http://localhost:8000")
    except:
        print("❌ No se pudo conectar al servidor")
        print("   Por favor, asegúrate de que el servidor esté corriendo:")
        print("   cd backend && ../venv/bin/python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Determinar el archivo de video a usar
    video_path = None
    
    if len(sys.argv) > 1:
        # Usuario proporcionó un archivo
        video_path = sys.argv[1]
    else:
        # Intentar crear video de prueba
        video_path = create_test_video()
    
    # Ejecutar prueba
    if video_path:
        test_analyze_endpoint(video_path)
    else:
        print("\n⚠️  No se proporcionó archivo de video")
        print("\nUso:")
        print(f"  python {sys.argv[0]} <ruta_al_video.mp4>")
        print("\nEjemplo:")
        print(f"  python {sys.argv[0]} mi_clase.mp4")

if __name__ == "__main__":
    main()
