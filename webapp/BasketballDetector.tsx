'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { Upload, Camera, AlertCircle, CheckCircle } from 'lucide-react'

interface Detection {
  bbox: {
    x1: number
    y1: number
    x2: number
    y2: number
    width: number
    height: number
    center_x: number
    center_y: number
  }
  class: string
  class_id: number
  confidence: number
  area: number
}

interface DetectionResponse {
  success: boolean
  detections: Detection[]
  count: number
  processing_time: number
  image_size: {
    width: number
    height: number
  }
  model: string
  timestamp: string
  error?: string
}

interface ModelInfo {
  loaded: boolean
  model_type: string
  classes: string[]
  load_time: number
  error?: string
}

const BasketballDetector: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<DetectionResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [confidence, setConfidence] = useState(0.25)
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null)
  
  // API base URL - adjust for your deployment
  const API_BASE_URL = process.env.NEXT_PUBLIC_BASKETBALL_API_URL || 'http://localhost:5000'

  useEffect(() => {
    loadModelInfo()
  }, [])

  const loadModelInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/model-info`)
      const info = await response.json()
      setModelInfo(info)
    } catch (err) {
      console.error('Failed to load model info:', err)
    }
  }

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file)
    setError(null)
    
    const reader = new FileReader()
    reader.onload = (e) => {
      setImagePreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0 && files[0].type.startsWith('image/')) {
      handleFileSelect(files[0])
    }
  }, [handleFileSelect])

  const analyzeImage = async () => {
    if (!selectedFile) {
      setError('Please select an image first!')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedFile)

      const response = await fetch(`${API_BASE_URL}/api/detect?confidence=${confidence}`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      
      if (data.success) {
        setResults(data)
      } else {
        setError(data.error)
      }
    } catch (err) {
      setError(`Analysis failed: ${err instanceof Error ? err.message : 'Unknown error'}`)
    } finally {
      setIsLoading(false)
    }
  }

  const clearResults = () => {
    setSelectedFile(null)
    setImagePreview(null)
    setResults(null)
    setError(null)
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.7) return 'bg-green-100 text-green-800'
    if (confidence > 0.5) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🏀 Basketball Object Detection
        </h1>
        <p className="text-gray-600">AI-powered basketball analysis system</p>
      </div>

      {/* Model Status */}
      {modelInfo && (
        <div className={`p-4 rounded-lg mb-6 ${
          modelInfo.loaded 
            ? 'bg-blue-50 border border-blue-200 text-blue-800' 
            : 'bg-red-50 border border-red-200 text-red-800'
        }`}>
          {modelInfo.loaded ? (
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              <div>
                <strong>{modelInfo.model_type}</strong> loaded successfully
                <div className="text-sm mt-1">
                  Classes: {modelInfo.classes.join(', ')} | Load time: {modelInfo.load_time?.toFixed(2)}s
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              <div>Model failed to load: {modelInfo.error}</div>
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        </div>
      )}

      {/* Upload Area */}
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors mb-6"
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => document.getElementById('fileInput')?.click()}
      >
        <Upload className="mx-auto mb-4 w-12 h-12 text-gray-400" />
        <div className="text-lg text-gray-600 mb-2">
          Click to upload or drag and drop an image
        </div>
        <div className="text-sm text-gray-500">
          Supports JPG, PNG, GIF, WebP (max 10MB)
        </div>
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
        />
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-center mb-6">
        <button
          onClick={analyzeImage}
          disabled={!selectedFile || isLoading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <Camera className="w-4 h-4" />
          {isLoading ? 'Analyzing...' : 'Analyze Image'}
        </button>
        
        <button
          onClick={clearResults}
          className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
        >
          Clear
        </button>

        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Confidence:</label>
          <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.05"
            value={confidence}
            onChange={(e) => setConfidence(parseFloat(e.target.value))}
            className="w-32"
          />
          <span className="text-sm text-gray-600">{confidence}</span>
        </div>
      </div>

      {/* Image Preview */}
      {imagePreview && (
        <div className="mb-6">
          <img
            src={imagePreview}
            alt="Preview"
            className="max-w-full max-h-96 mx-auto rounded-lg shadow-md"
          />
        </div>
      )}

      {/* Loading */}
      {isLoading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Analyzing image...</p>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="border-t pt-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Detection Results</h3>
            <div className="flex gap-4 text-sm text-gray-600">
              <span>{results.count} objects</span>
              <span>{(results.processing_time * 1000).toFixed(0)}ms</span>
            </div>
          </div>

          {results.detections.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No objects detected. Try lowering the confidence threshold.
            </div>
          ) : (
            <div className="space-y-4">
              {results.detections.map((detection, index) => (
                <div
                  key={index}
                  className="bg-gray-50 border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                >
                  <div className="flex justify-between items-center mb-3">
                    <div className="font-semibold text-gray-900">
                      #{index + 1} {detection.class}
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(detection.confidence)}`}>
                      {(detection.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                    <div>
                      <strong>Position:</strong> ({detection.bbox.x1}, {detection.bbox.y1})
                    </div>
                    <div>
                      <strong>Size:</strong> {detection.bbox.width}×{detection.bbox.height}
                    </div>
                    <div>
                      <strong>Area:</strong> {detection.area.toLocaleString()}px²
                    </div>
                    <div>
                      <strong>Center:</strong> ({detection.bbox.center_x}, {detection.bbox.center_y})
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default BasketballDetector 