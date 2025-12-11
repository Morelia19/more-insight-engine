-- More Insight Engine - Database Schema
-- Execute este SQL en el SQL Editor de Supabase

-- Tabla de Videos
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    filename VARCHAR(255) NOT NULL,
    duration FLOAT NOT NULL,
    storage_url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de Sesiones/Reportes
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    video_id UUID REFERENCES videos (id) ON DELETE CASCADE,
    student_name VARCHAR(255) NOT NULL,
    teacher_name VARCHAR(255) NOT NULL,
    session_photo_url TEXT,
    transcript_text TEXT,
    analysis_json JSONB,
    report_image_url TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, error
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_sessions_video_id ON sessions (video_id);

CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions (status);

CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions (created_at DESC);

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios para documentación
COMMENT ON TABLE videos IS 'Almacena metadatos de videos subidos';

COMMENT ON TABLE sessions IS 'Almacena sesiones de análisis pedagógico con sus resultados';