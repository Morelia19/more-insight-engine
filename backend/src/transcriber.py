import os
from groq import Groq

class AudioTranscriber:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Please add your API key to the .env file. "
                "Get one free at: https://console.groq.com"
            )
        self.client = Groq(api_key=api_key)
        print("✅ Groq Whisper API initialized")
    
    def transcribe(self, audio_path: str) -> str:
        print(f"🎤 Transcribing with Groq Whisper: {audio_path}")
        
        try:
            file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            print(f"📊 File size: {file_size_mb:.2f} MB")
            
            if file_size_mb < 20:
                return self._transcribe_file(audio_path)
            
            print(f"⚠️  Large file ({file_size_mb:.2f}MB), splitting into chunks...")
            return self._transcribe_large_file(audio_path)
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return ""
    
    def _transcribe_file(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                language="es",
                response_format="text",
                temperature=0.0
            )
        
        transcript = transcription.strip()
        print(f"✅ Transcription completed: {len(transcript)} characters")
        
        if len(transcript) > 0:
            print(f"📄 First 200 characters: {transcript[:200]}...")
        
        return transcript
    
    def _transcribe_large_file(self, audio_path: str) -> str:
        from pydub import AudioSegment
        import math
        
        audio = AudioSegment.from_file(audio_path)
        duration_ms = len(audio)
        duration_min = duration_ms / (1000 * 60)
        
        print(f"⏱️  Audio duration: {duration_min:.1f} minutes")
        
        chunk_length_ms = 10 * 60 * 1000
        num_chunks = math.ceil(duration_ms / chunk_length_ms)
        
        print(f"🔪 Splitting into {num_chunks} chunks of ~10 minutes...")
        
        transcripts = []
        
        for i in range(num_chunks):
            start_ms = i * chunk_length_ms
            end_ms = min((i + 1) * chunk_length_ms, duration_ms)
            
            print(f"📝 Processing chunk {i+1}/{num_chunks} ({start_ms//1000//60}:{start_ms//1000%60:02d} - {end_ms//1000//60}:{end_ms//1000%60:02d})...")
            
            chunk = audio[start_ms:end_ms]
            chunk_path = f"temp_chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            try:
                chunk_transcript = self._transcribe_file(chunk_path)
                transcripts.append(chunk_transcript)
            except Exception as e:
                print(f"⚠️  Error in chunk {i+1}: {e}")
                transcripts.append("")
            finally:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
        
        full_transcript = " ".join(transcripts)
        print(f"✅ Complete transcription: {len(full_transcript)} characters ({num_chunks} chunks)")
        
        return full_transcript
