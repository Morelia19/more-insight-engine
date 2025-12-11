import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class PedagogicalAnalyzer:
    def __init__(self):
        model_id = "deepseek-ai/DeepSeek-V2-Lite-Chat"
        print(f"🧠 Cargando DeepSeek V2 Lite ({model_id})...")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )

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

        inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            inputs, 
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7 # Creatividad controlada
        )
        
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response