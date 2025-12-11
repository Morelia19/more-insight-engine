import whisper
import torch

class AudioTranscriber:
    def __init__(self, model_size="small"):
        """
        Carga Whisper.
        Usa "small" para pruebas rápidas o "medium" para mayor precisión en tesis.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎧 Cargando Whisper ({model_size}) en {device}...")
        self.model = whisper.load_model(model_size, device=device)

    def transcribe(self, audio_path):
        print(f"⏳ Transcribiendo: {audio_path}...")
        # fp16=False evita errores en algunas CPUs/GPUs viejas
        result = self.model.transcribe(audio_path, language="es", fp16=False)
        return result["text"]