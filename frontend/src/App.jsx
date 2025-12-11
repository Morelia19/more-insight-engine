import { useState } from 'react'
import { Upload, Loader2, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'
import './index.css'

function App() {
  const [videoFile, setVideoFile] = useState(null)
  const [sessionPhoto, setSessionPhoto] = useState(null)
  const [teacherName, setTeacherName] = useState('Profesor')
  const [studentName, setStudentName] = useState('Estudiante')
  const [loading, setLoading] = useState(false)
  const [analysisData, setAnalysisData] = useState(null)
  const [editableAnalysis, setEditableAnalysis] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [generatingReport, setGeneratingReport] = useState(false)

  const handleVideoChange = (e) => {
    setVideoFile(e.target.files[0])
    setError(null)
    setAnalysisData(null)
    setEditableAnalysis(null)
    setResult(null)
  }

  const handleSessionPhotoChange = (e) => {
    setSessionPhoto(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!videoFile) {
      setError('Por favor selecciona un archivo de video')
      return
    }

    setLoading(true)
    setError(null)
    setAnalysisData(null)
    setEditableAnalysis(null)
    setResult(null)

    const formData = new FormData()
    formData.append('video', videoFile)

    if (sessionPhoto) {
      formData.append('session_photo', sessionPhoto)
    }

    formData.append('teacher_name', teacherName)
    formData.append('student_name', studentName)

    try {
      const response = await axios.post('http://localhost:8000/analyze_class', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      // Guardar análisis para edición
      setAnalysisData(response.data)
      setEditableAnalysis(JSON.stringify(response.data.report, null, 2))
    } catch (err) {
      setError(err.response?.data?.message || 'Error al procesar el archivo')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReport = async () => {
    setGeneratingReport(true)
    setError(null)

    try {
      // Parsear el análisis editado
      const editedReport = JSON.parse(editableAnalysis)

      const formData = new FormData()
      formData.append('analysis', JSON.stringify(editedReport))

      if (sessionPhoto) {
        formData.append('session_photo', sessionPhoto)
      }

      formData.append('teacher_name', teacherName)
      formData.append('student_name', studentName)

      const response = await axios.post('http://localhost:8000/generate_report', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResult(response.data)
    } catch (err) {
      if (err instanceof SyntaxError) {
        setError('Error: El análisis no es un JSON válido')
      } else {
        setError(err.response?.data?.message || 'Error al generar el reporte')
      }
    } finally {
      setGeneratingReport(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            More Insight
          </h1>
          <p className="text-lg text-gray-600">
            Auditoría Pedagógica Automatizada con IA
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Nombres */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Estudiante
                </label>
                <input
                  type="text"
                  value={studentName}
                  onChange={(e) => setStudentName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
                  placeholder="Nombre del estudiante"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Profesor
                </label>
                <input
                  type="text"
                  value={teacherName}
                  onChange={(e) => setTeacherName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
                  placeholder="Nombre del profesor"
                />
              </div>
            </div>

            {/* Video Upload */}
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-indigo-500 transition-colors">
              <Upload className="mx-auto h-10 w-10 text-gray-400 mb-3" />
              <label htmlFor="video-upload" className="cursor-pointer">
                <span className="text-indigo-600 hover:text-indigo-500 font-medium">
                  Seleccionar archivo de video
                </span>
                <input
                  id="video-upload"
                  type="file"
                  accept="video/*"
                  className="sr-only"
                  onChange={handleVideoChange}
                />
              </label>
              {videoFile && (
                <p className="mt-2 text-sm text-gray-600">
                  🎥 {videoFile.name}
                </p>
              )}
            </div>

            {/* Photos Grid */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Foto de la Sesión (Opcional)
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-indigo-500 transition-colors">
                <label htmlFor="session-photo" className="cursor-pointer">
                  {sessionPhoto ? (
                    <div>
                      <img
                        src={URL.createObjectURL(sessionPhoto)}
                        alt="Preview"
                        className="mx-auto h-32 w-auto rounded-lg mb-2 object-cover"
                      />
                      <p className="text-xs text-gray-600">Cambiar foto</p>
                    </div>
                  ) : (
                    <div>
                      <Upload className="mx-auto h-10 w-10 text-gray-400 mb-2" />
                      <span className="text-sm text-indigo-600">Subir foto de la sesión</span>
                      <p className="text-xs text-gray-500 mt-1">Captura horizontal con profesor y alumno</p>
                    </div>
                  )}
                  <input
                    id="session-photo"
                    type="file"
                    accept="image/*"
                    className="sr-only"
                    onChange={handleSessionPhotoChange}
                  />
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !videoFile}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Analizando...
                </>
              ) : (
                'Analizar Clase'
              )}
            </button>
          </form>

          {error && (
            <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
              <XCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-red-900">Error</h3>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Paso 1: Mostrar análisis editable */}
          {analysisData && !result && (
            <div className="mt-6 space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium text-blue-900 mb-2">✅ Análisis Completado</h3>
                <p className="text-blue-700 text-sm">Revisa el contenido y edítalo si es necesario. Luego genera el reporte visual.</p>
              </div>

              {/* Transcripción */}
              <details className="bg-gray-50 rounded-lg p-4">
                <summary className="cursor-pointer font-semibold text-gray-900">Ver transcripción</summary>
                <p className="text-gray-600 text-sm mt-3 leading-relaxed">{analysisData.transcript}</p>
              </details>

              {/* Análisis editable */}
              <div className="bg-white rounded-lg p-6 border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-3">Análisis Pedagógico (Editable)</h3>
                <textarea
                  value={editableAnalysis}
                  onChange={(e) => setEditableAnalysis(e.target.value)}
                  className="w-full h-96 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900"
                  placeholder="Análisis en formato JSON..."
                />
                <p className="text-xs text-gray-500 mt-2">💡 Puedes editar directamente el JSON antes de generar el reporte</p>
              </div>

              {/* Botón generar reporte */}
              <button
                onClick={handleGenerateReport}
                disabled={generatingReport}
                className="w-full bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {generatingReport ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generando Reporte Visual...
                  </>
                ) : (
                  '🎨 Generar Reporte Visual'
                )}
              </button>
            </div>
          )}

          {/* Paso 2: Mostrar reporte generado */}
          {result?.status === 'success' && (
            <div className="mt-6 space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-medium text-green-900">¡Reporte Generado!</h3>
                  <p className="text-green-700 text-sm mt-1">El análisis se completó exitosamente</p>
                </div>
              </div>

              {/* Imagen del Reporte */}
              {result.report_image && (
                <div className="bg-white rounded-lg p-4 border border-gray-200">
                  <h3 className="font-semibold text-gray-900 mb-3">Reporte Visual:</h3>
                  <img
                    src={`http://localhost:8000${result.report_image}`}
                    alt="Reporte Pedagógico"
                    className="w-full rounded-lg shadow-lg"
                  />
                  <a
                    href={`http://localhost:8000${result.report_image}`}
                    download
                    className="mt-4 inline-block w-full text-center bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors"
                  >
                    📥 Descargar Reporte
                  </a>
                </div>
              )}

              {/* Datos adicionales (colapsable) */}
              <details className="bg-gray-50 rounded-lg p-6">
                <summary className="cursor-pointer font-semibold text-gray-900 mb-2">Ver transcripción y datos</summary>
                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Transcripción:</h4>
                    <p className="text-gray-600 text-sm leading-relaxed">{result.transcript}</p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Datos del Análisis:</h4>
                    <pre className="bg-white p-4 rounded border border-gray-200 overflow-x-auto text-xs">
                      {JSON.stringify(result.report, null, 2)}
                    </pre>
                  </div>
                </div>
              </details>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
