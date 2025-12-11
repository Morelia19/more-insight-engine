import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional, Dict, Any

load_dotenv()

class DatabaseService:
    def __init__(self):
        """Initialize Supabase client for database operations"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        print(f"✅ Database service initialized")
    
    # ========== VIDEO OPERATIONS ==========
    
    def create_video(self, filename: str, duration: float, storage_url: str) -> Dict[str, Any]:
        """Create a new video record"""
        try:
            result = self.client.table('videos').insert({
                'filename': filename,
                'duration': duration,
                'storage_url': storage_url
            }).execute()
            return result.data[0]
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            raise
    
    def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video by ID"""
        try:
            result = self.client.table('videos')\
                .select('*')\
                .eq('id', video_id)\
                .single()\
                .execute()
            return result.data
        except Exception as e:
            print(f"❌ Error getting video: {e}")
            return None
    
    # ========== SESSION OPERATIONS ==========
    
    def create_session(
        self, 
        video_id: str,
        student_name: str,
        teacher_name: str,
        session_photo_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new session record"""
        try:
            result = self.client.table('sessions').insert({
                'video_id': video_id,
                'student_name': student_name,
                'teacher_name': teacher_name,
                'session_photo_url': session_photo_url,
                'status': 'pending'
            }).execute()
            return result.data[0]
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            raise
    
    def update_session_transcript(self, session_id: str, transcript: str):
        """Update session with transcript"""
        try:
            self.client.table('sessions').update({
                'transcript_text': transcript,
                'status': 'processing'
            }).eq('id', session_id).execute()
            print(f"✅ Transcript saved for session {session_id}")
        except Exception as e:
            print(f"❌ Error updating transcript: {e}")
            raise
    
    def update_session_analysis(self, session_id: str, analysis: Dict[str, Any]):
        """Update session with analysis JSON"""
        try:
            self.client.table('sessions').update({
                'analysis_json': analysis,
                'status': 'processing'
            }).eq('id', session_id).execute()
            print(f"✅ Analysis saved for session {session_id}")
        except Exception as e:
            print(f"❌ Error updating analysis: {e}")
            raise
    
    def update_session_report(self, session_id: str, report_url: str):
        """Update session with report image URL"""
        try:
            self.client.table('sessions').update({
                'report_image_url': report_url,
                'status': 'completed'
            }).eq('id', session_id).execute()
            print(f"✅ Report saved for session {session_id}")
        except Exception as e:
            print(f"❌ Error updating report: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID with video data"""
        try:
            result = self.client.table('sessions')\
                .select('*, video:videos(*)')\
                .eq('id', session_id)\
                .single()\
                .execute()
            return result.data
        except Exception as e:
            print(f"❌ Error getting session: {e}")
            return None
    
    def get_all_sessions(self, limit: int = 50) -> list:
        """Get all sessions with pagination"""
        try:
            result = self.client.table('sessions')\
                .select('*, video:videos(*)')\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"❌ Error getting sessions: {e}")
            return []
    
    def update_session_error(self, session_id: str, error_message: str):
        """Mark session as error"""
        try:
            self.client.table('sessions').update({
                'status': 'error',
                'analysis_json': {'error': error_message}
            }).eq('id', session_id).execute()
            print(f"⚠️ Session {session_id} marked as error")
        except Exception as e:
            print(f"❌ Error updating session error: {e}")

# Global instance
db_service = DatabaseService() if os.getenv("SUPABASE_URL") else None
