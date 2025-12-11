import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class PedagogicalAnalyzer:
    def __init__(self):
        model_id = "microsoft/Phi-3-mini-4k-instruct"
        print(f"🧠 Cargando Phi-3 Mini ({model_id})...")
        print("✅ Modelo optimizado: ~7.6 GB, excelente para análisis pedagógico")

        # Detectar el dispositivo disponible
        if torch.backends.mps.is_available():
            device = "mps"
            print("✅ Usando aceleración MPS (Apple Silicon)")
        elif torch.cuda.is_available():
            device = "cuda"
            print("✅ Usando aceleración CUDA")
        else:
            device = "cpu"
            print("⚠️  Usando CPU (más lento)")

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,  # Usar float16 para reducir uso de RAM
            low_cpu_mem_usage=True,
            trust_remote_code=True
        ).to(device)
        
        self.device = device

    def analyze_class(self, transcription):
        # PROMPT DE AUDITORÍA PEDAGÓGICA (Tu aporte intelectual)
        system_prompt = (
            "Eres 'More Insight', un auditor experto de calidad educativa en More Academy. "
            "Tu tarea es analizar la siguiente transcripción de una clase y generar un reporte JSON estricto. "
            "Evalúa: 1. Puntualidad/Asistencia, 2. Participación del alumno, 3. Logro de objetivos, 4. Actitud (0-100). "
            "Responde SOLAMENTE con el JSON, sin texto adicional."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Transcripción:\n{transcription}"}
        ]

        inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            inputs, 
            max_new_tokens=512,  # Reducido: suficiente para JSON de reporte
            do_sample=True,
            temperature=0.7 
        )
        
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response