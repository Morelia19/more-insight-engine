import os
import json
from groq import Groq

class PedagogicalAnalyzer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Please add your API key to the .env file"
            )
        
        self.client = Groq(api_key=api_key)
        print("✅ Groq API initialized")
    
    def analyze_class(self, transcript: str) -> dict:
        print("🧠 Analyzing class...")
        print(f"💭 Generating analysis with Groq ({len(transcript)} characters)...")
        
        prompt = self._build_prompt(transcript)
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=1500,
            )
            
            response = chat_completion.choices[0].message.content
            
            tokens_used = chat_completion.usage.total_tokens
            print(f"✅ Analysis generated in ~{tokens_used} tokens")
            print(f"📄 Model response:\n{response[:200]}...")
            
            analysis = self._extract_json(response)
            
            if self._validate_analysis(analysis):
                print("✅ Valid JSON with all fields")
                return analysis
            else:
                print("⚠️  Invalid JSON structure")
                return self._get_default_analysis()
                
        except Exception as e:
            print(f"❌ Error in analysis: {e}")
            return self._get_default_analysis()
    
    def _build_prompt(self, transcript: str) -> str:
        return f"""Eres un analista pedagógico experto. Analiza esta transcripción de clase y genera un análisis en formato JSON.

IMPORTANTE: Responde ÚNICAMENTE con el objeto JSON, sin texto adicional antes o después.

Estructura JSON requerida:
{{
  "objetivos": ["objetivo 1", "objetivo 2", "objetivo 3"],
  "desarrollo": "resumen detallado de la clase en máximo 200 palabras",
  "actitud": "descripción textual de la actitud y participación de los estudiantes (ej: 'Excelente actitud. Muy participativo y enfocado.')",
  "recomendaciones": "recomendaciones para mejorar en máximo 150 palabras"
}}

TRANSCRIPCIÓN DE LA CLASE:
{transcript}

Genera ahora el análisis en JSON puro (sin markdown, sin explicaciones):"""
    
    def _extract_json(self, response: str) -> dict:
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            analysis = json.loads(response)
            print(f"📊 JSON extracted:\n{json.dumps(analysis, indent=2, ensure_ascii=False)}")
            return analysis
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error: {e}")
            return self._get_default_analysis()
    
    def _validate_analysis(self, analysis: dict) -> bool:
        required_keys = ['objetivos', 'desarrollo', 'actitud', 'recomendaciones']
        return all(key in analysis for key in required_keys)
    
    def _get_default_analysis(self) -> dict:
        return {
            "objetivos": ["Revisar contenido de la clase", "Fomentar participación", "Evaluar comprensión"],
            "desarrollo": "Clase enfocada en el aprendizaje activo y la participación de los estudiantes.",
            "actitud": "Actitud positiva y participativa durante la sesión.",
            "recomendaciones": "Continuar fomentando la participación activa y el diálogo en clase."
        }