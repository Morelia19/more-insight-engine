import torch
import json
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

    def analyze_class(self, transcript: str) -> str:
        """
        Analiza la transcripción de una clase usando Phi-3-mini
        """
        # Truncar transcripción si es muy larga (límite: ~3000 tokens ≈ 12000 caracteres)
        max_chars = 12000
        if len(transcript) > max_chars:
            print(f"⚠️  Transcripción muy larga ({len(transcript)} chars), truncando a {max_chars} chars")
            # Tomar inicio y final
            chunk_size = max_chars // 2
            transcript = transcript[:chunk_size] + "\n...[contenido omitido]...\n" + transcript[-chunk_size:]
        
        prompt = f"""Eres un analista pedagógico experto. Analiza esta clase y genera un reporte estructurado en formato JSON con los siguientes campos:

1. "objetivos": Lista de 2-3 objetivos principales de la sesión
2. "desarrollo": Resumen del desarrollo de la clase (máximo 200 palabras)
3. "actitud": Puntaje de actitud del estudiante (0-100)
4. "recomendaciones": Recomendaciones para futuras sesiones (máximo 150 palabras)

Transcripción de la clase:
{transcript}

Genera SOLO el JSON, sin texto adicional:"""

        try:
            print(f"💭 Generando análisis ({len(transcript)} caracteres)...")
            
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=3500).to(self.device)
            
            # Generar con configuración optimizada
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=800,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    use_cache=False  # Desactivar cache para evitar error DynamicCache
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extraer solo la respuesta (después del prompt)
            if prompt in response:
                response = response.split(prompt)[-1].strip()
            
            print(f"✅ Análisis generado: {len(response)} caracteres")
            return response
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            # Retornar estructura básica en caso de error
            return json.dumps({
                "objetivos": ["Análisis de la clase"],
                "desarrollo": f"Error al analizar: {str(e)}",
                "actitud": 75,
                "recomendaciones": "Revisar transcripción y volver a analizar."
            }, ensure_ascii=False)