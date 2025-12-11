import { useState } from 'react'
import { Upload, Loader2, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
    setResult(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Por favor selecciona un archivo de audio')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:8000/process_class', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.message || 'Error al procesar el archivo')
    } finally {
      setLoading(false)
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
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-indigo-500 transition-colors">
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-indigo-600 hover:text-indigo-500 font-medium">
                  Seleccionar archivo de audio
                </span>
                <input
                  id="file-upload"
                  name="file-upload"
                  type="file"
                  accept="audio/*"
                  className="sr-only"
                  onChange={handleFileChange}
                />
              </label>
              {file && (
                <p className="mt-2 text-sm text-gray-600">
                  Archivo: {file.name}
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Procesando...
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

          {result?.status === 'success' && (
            <div className="mt-6 space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-medium text-green-900">¡Análisis Completado!</h3>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 space-y-4">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Transcripción:</h3>
                  <p className="text-gray-700 leading-relaxed">{result.transcript}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Reporte Pedagógico:</h3>
                  <pre className="bg-white p-4 rounded border border-gray-200 overflow-x-auto text-sm">
                    {JSON.stringify(result.report, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
