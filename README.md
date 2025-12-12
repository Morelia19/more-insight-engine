# More Insight Engine

Automated pedagogical analysis system powered by AI. Transcribe class videos, analyze teaching sessions, and generate professional visual reports automatically.

![More Insight Engine](https://img.shields.io/badge/Status-Ready-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18+-61DAFB)

## Features

- **Fast transcription** with Groq Whisper API (~3-4 min for 90-min videos)
- **AI-powered analysis** using Llama 3.3 70B for pedagogical insights
- **Editable analysis** - review and modify AI-generated content
- **Professional reports** - dynamic PDF-like reports with custom branding
- **Logo customization** - upload your institution's logo
- **Session management** - track session numbers and dates
- **Structured analysis** - objectives, development, attitude, recommendations

## Tech Stack

**Backend:**
- FastAPI - High-performance Python web framework
- Groq API - Ultra-fast AI inference (Whisper + Llama)
- Pillow - Report generation
- FFmpeg - Audio extraction

**Frontend:**
- React + Vite - Modern UI framework
- Tailwind CSS - Utility-first styling
- Axios - HTTP client
- Lucide React - Icon library

## Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/more-insight-engine.git
cd more-insight-engine
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Configuration

Create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com)

## Usage

### Start the Backend

```bash
cd backend
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

### Start the Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Using the Application

1. **Upload a Video** - Select your class recording
2. **Fill Details** - Student name, teacher name, session info
3. **Add Media** (Optional) - Session photo and institutional logo
4. **Analyze** - AI processes the video and generates analysis
5. **Review & Edit** - Modify the AI-generated analysis as needed
6. **Generate Report** - Create professional visual report

## Project Structure

```
more-insight-engine/
├── backend/
│   ├── src/
│   │   ├── analyzer.py          # AI analysis with Groq Llama
│   │   ├── transcriber.py       # Audio transcription with Groq Whisper
│   │   └── report_generator.py  # Visual report generation
│   ├── api.py                   # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisForm.jsx    # Editable analysis fields
│   │   │   ├── FileUpload.jsx      # Reusable file upload
│   │   │   ├── FormHeader.jsx      # App header
│   │   │   └── StatusMessage.jsx   # Status notifications
│   │   ├── App.jsx              # Main application
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API Endpoints

### `POST /analyze_class`
Analyzes a class video and returns transcription + AI analysis

**Parameters:**
- `video` (file) - Video file
- `teacher_name` (string)
- `student_name` (string)
- `session_number` (int)
- `total_sessions` (int)
- `session_date` (string, YYYY-MM-DD)

**Response:**
```json
{
  "transcript": "...",
  "report": {
    "objetivos": ["...", "...", "..."],
    "desarrollo": "...",
    "actitud": "...",
    "recomendaciones": "..."
  }
}
```

### `POST /generate_report`
Generates a visual report from analysis data

**Parameters:**
- `analysis` (JSON string) - Analysis data
- `session_photo` (file, optional) - Session photo
- `logo` (file, optional) - Institution logo
- `student_name` (string)
- `teacher_name` (string)
- `session_number` (int)
- `total_sessions` (int)
- `session_date` (string)

**Response:**
```json
{
  "status": "success",
  "report_image": "/reports/report_20231211_123456.png"
}
```

## Performance

- **Short videos (5-10 min)**: ~1-2 minutes
- **Medium videos (30-45 min)**: ~2-3 minutes  
- **Long videos (90 min)**: ~3-4 minutes

*Performance depends on Groq API rate limits (free tier: 7200 seconds/hour)*

## Groq API Limits

**Free Tier:**
- 7200 seconds of audio transcription per hour
- 30 requests per minute

For production use, consider upgrading to [Groq Dev Tier](https://console.groq.com/settings/billing)

**Estimated Costs (Dev Tier):**
- Transcription: $0.111 per hour
- Analysis: ~$0.001 per analysis
- **Total per 90-min video**: ~$0.15-0.20

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Groq](https://groq.com) for ultra-fast AI inference
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [React](https://react.dev/) for the UI framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

## Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/yourusername/more-insight-engine/issues)
- Check existing issues for solutions

---

Made with ❤️ for educators