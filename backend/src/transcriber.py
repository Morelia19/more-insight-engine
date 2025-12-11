import whisper
import torch

class AudioTranscriber:
    def __init__(self, model_size="tiny"):  # Optimizado: tiny (39 MB) vs small (244 MB)
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        
        print(f"Cargando Whisper ({model_size}) en {device}...")
        self.model = whisper.load_model(model_size, device=device)

    def transcribe(self, audio_path):
        print(f"Transcribiendo: {audio_path}...")
        result = self.model.transcribe(audio_path, language="es", fp16=False)
        return result["text"]