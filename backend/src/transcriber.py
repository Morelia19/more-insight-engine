from faster_whisper import WhisperModel
import torch

class AudioTranscriber:
    def __init__(self, model_size="tiny"):
        """
        Inicializa Faster-Whisper con aceleración MPS/GPU
        model_size: tiny, base, small, medium, large-v2
        """
        print(f"Cargando Faster-Whisper ({model_size}) con aceleración...")
        
        # Detectar dispositivo (MPS para Apple Silicon, CUDA para NVIDIA, CPU como fallback)
        if torch.backends.mps.is_available():
            device = "auto"  # faster-whisper auto-detecta MPS en Apple Silicon
            compute_type = "int8"  # Optimizado para Apple Silicon
            print("✅ Usando aceleración Apple Silicon (MPS)")
        elif torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
            print("✅ Usando aceleración NVIDIA (CUDA)")
        else:
            device = "cpu"
            compute_type = "int8"
            print("⚠️  Usando CPU (más lento)")
        
        # Cargar modelo optimizado
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
            num_workers=4  # Procesamiento paralelo
        )
        print(f"✅ Faster-Whisper cargado (~4-5x más rápido que Whisper normal)")
    
    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe un archivo de audio a texto
        """
        print(f"🎤 Transcribiendo: {audio_path}")
        
        # Transcribir con faster-whisper
        segments, info = self.model.transcribe(
            audio_path,
            language="es",  # Español
            beam_size=5,
            vad_filter=True,  # Filtro de detección de voz (más rápido)
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        # Detectar idioma
        print(f"📝 Idioma detectado: {info.language} ({info.language_probability:.2%} confianza)")
        print(f"⏱️  Duración del audio: {info.duration:.1f} segundos")
        
        # Unir todos los segmentos
        transcript = " ".join([segment.text for segment in segments])
        
        print(f"✅ Transcripción completada: {len(transcript)} caracteres")
        return transcript.strip()
