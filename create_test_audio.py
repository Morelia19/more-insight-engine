#!/usr/bin/env python3
"""
Genera un video de prueba simple usando una grabación de texto a voz
"""
import wave
import struct
import math

def create_test_audio(filename="test_audio.wav", duration=5):
    """Crea un archivo de audio WAV de prueba"""
    sample_rate = 16000
    frequency = 440  # La4 - 440 Hz
    num_samples = duration * sample_rate
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generar tono senoidal
        for i in range(num_samples):
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('h', value))
    
    print(f"✅ Audio de prueba creado: {filename}")
    return filename

if __name__ == "__main__":
    create_test_audio()
