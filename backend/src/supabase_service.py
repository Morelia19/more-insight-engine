import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        print(f"✅ Supabase client initialized: {supabase_url}")
    
    async def upload_video(self, file_path: str, filename: str) -> str:
        """Upload video to Supabase Storage"""
        try:
            with open(file_path, 'rb') as f:
                response = self.client.storage.from_('videos').upload(
                    filename,
                    f,
                    file_options={"content-type": "video/mp4"}
                )
            
            # Get public URL
            url = self.client.storage.from_('videos').get_public_url(filename)
            print(f"✅ Video uploaded: {url}")
            return url
        except Exception as e:
            print(f"❌ Error uploading video: {e}")
            raise
    
    async def upload_report(self, file_path: str, filename: str) -> str:
        """Upload report image to Supabase Storage"""
        try:
            with open(file_path, 'rb') as f:
                response = self.client.storage.from_('reports').upload(
                    filename,
                    f,
                    file_options={"content-type": "image/png"}
                )
            
            # Get public URL
            url = self.client.storage.from_('reports').get_public_url(filename)
            print(f"✅ Report uploaded: {url}")
            return url
        except Exception as e:
            print(f"❌ Error uploading report: {e}")
            raise
    
    async def upload_session_photo(self, file_path: str, filename: str) -> str:
        """Upload session photo to Supabase Storage"""
        try:
            with open(file_path, 'rb') as f:
                response = self.client.storage.from_('session-photos').upload(
                    filename,
                    f,
                    file_options={"content-type": "image/jpeg"}
                )
            
            # Get public URL
            url = self.client.storage.from_('session-photos').get_public_url(filename)
            print(f"✅ Session photo uploaded: {url}")
            return url
        except Exception as e:
            print(f"❌ Error uploading session photo: {e}")
            raise
    
    def download_video(self, filename: str, destination: str):
        """Download video from Supabase Storage"""
        try:
            response = self.client.storage.from_('videos').download(filename)
            with open(destination, 'wb') as f:
                f.write(response)
            print(f"✅ Video downloaded: {destination}")
        except Exception as e:
            print(f"❌ Error downloading video: {e}")
            raise

# Global instance
supabase_service = SupabaseService() if os.getenv("SUPABASE_URL") else None
