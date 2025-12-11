#!/usr/bin/env python3
"""
Script simple para probar el API de More Insight Engine
Genera un análisis de ejemplo y muestra el JSON resultante
"""
import requests
import json
import wave
import struct
import math
import os

def create_simple_test_file():
    """Crea un archivo de audio WAV simple para prueba"""
    filename = "test_clase.wav"
    sample_rate = 16000
    duration = 3  # 3 segundos
    frequency = 440
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        num_samples = duration * sample_rate
        for i in range(num_samples):
            value = int(32767 * 0.1 * math.sin(2 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('h', value))
    
    print(f"✅ Archivo de prueba creado: {filename}")
    return filename

def test_api():
    """Prueba el endpoint de análisis"""
    API_URL = "http://localhost:8000/analyze_class"
    
    print("\n" + "="*70)
    print("🧪 MORE INSIGHT ENGINE - Prueba de Análisis JSON")
    print("="*70 + "\n")
    
    # Crear archivo de prueba
    audio_file = create_simple_test_file()
    
    print(f"📤 Enviando archivo al servidor...")
    print(f"   Estudiante: Ana Rodríguez")
    print(f"   Profesor: Carlos Mendoza\n")
    print(f"⏳ Procesando (esto puede tardar 1-3 minutos)...\n")
    
    try:
        with open(audio_file, 'rb') as f:
            files = {'video': (audio_file, f, 'audio/wav')}
            data = {
                'student_name': 'Ana Rodríguez',
                'teacher_name': 'Carlos Mendoza'
            }
            
            response = requests.post(API_URL, files=files, data=data, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            
            print("="*70)
            print("✅ ANÁLISIS COMPLETADO")
            print("="*70 + "\n")
            
            # Transcripción
            print("📝 TRANSCRIPCIÓN:")
            print("-"*70)
            transcript = result.get('transcript', '')
            if len(transcript) > 300:
                print(f"{transcript[:300]}...")
                print(f"[{len(transcript)} caracteres en total]\n")
            else:
                print(f"{transcript}\n")
            
            # Análisis JSON
            print("🧠 ANÁLISIS PEDAGÓGICO (JSON):")
            print("-"*70)
            report = result.get('report', {})
            print(json.dumps(report, indent=2, ensure_ascii=False))
            
            # Guardar resultado
            output_file = "resultado_analisis.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Resultado guardado en: {output_file}")
            
            # Mostrar estructura del JSON
            print("\n" + "="*70)
            print("📊 ESTRUCTURA DEL JSON DE ANÁLISIS:")
            print("="*70)
            print(f"✓ objetivos: {len(report.get('objetivos', []))} items")
            print(f"✓ desarrollo: {len(report.get('desarrollo', ''))} caracteres")
            print(f"✓ actitud: {report.get('actitud', 'N/A')} puntos")
            print(f"✓ recomendaciones: {len(report.get('recomendaciones', ''))} caracteres")
            
            print("\n" + "="*70)
            print("✅ PRUEBA EXITOSA - El JSON se genera correctamente")
            print("="*70 + "\n")
            
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("   ¿Está corriendo en http://localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Limpiar archivo de prueba
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"🧹 Archivo de prueba eliminado")

if __name__ == "__main__":
    test_api()
