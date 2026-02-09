'use client'

import React, { useState } from 'react'
import { Upload, FileText, Send, Download, Settings } from 'lucide-react'
import { API_BASE_URL } from '../config/api'
import SummarizerForm from '@/components/SummarizerForm'
import SummaryResult from '@/components/SummaryResult'
import { Brain, Sparkles, Zap, Shield } from 'lucide-react'

interface SummarizationRequest {
  text: string
  method: 'extractive' | 'abstractive' | 'hybrid'
  model: 'bart' | 't5' | 'pegasus' | 'openai' | 'cohere'
  max_sentences: number
  max_length: number
  min_length: number
}

interface SummarizationResult {
  summary: string
  method: string
  model: string
  original_length: number
  summary_length: number
  compression_ratio: number
  processing_time: number
}

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SummarizationResult | null>(null)

  const handleSummarize = async (request: SummarizationRequest) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/summarize/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        const error = await response.json()
        alert(`Error: ${error.detail || 'Failed to summarize text'}`)
      }
    } catch (error) {
      alert('Network error. Please check if the backend server is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format: string) => {
    if (!result) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/export/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: result.summary,
          filename: 'summary',
          format: format,
          include_metadata: true,
          metadata: {
            original_length: result.original_length,
            summary_length: result.summary_length,
            compression_ratio: result.compression_ratio,
            processing_time: result.processing_time,
            method: result.method,
            model: result.model
          }
        }),
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `summary.${format}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        alert('Failed to export summary')
      }
    } catch (error) {
      alert('Error exporting summary')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Brain className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">AI Text Summarizer</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">Powered by Advanced AI</span>
              <Sparkles className="w-5 h-5 text-yellow-500" />
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Transform Long Text into Clear, Concise Summaries
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Our AI-powered summarizer uses cutting-edge machine learning models to extract key information 
            and generate high-quality summaries in seconds.
          </p>
          
          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white rounded-lg p-6 shadow-lg">
              <Zap className="w-8 h-8 text-yellow-500 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Lightning Fast</h3>
              <p className="text-gray-600">Get summaries in seconds with our optimized AI models</p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-lg">
              <Brain className="w-8 h-8 text-blue-500 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Multiple AI Models</h3>
              <p className="text-gray-600">Choose from BART, T5, PEGASUS, OpenAI, and Cohere models</p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-lg">
              <Shield className="w-8 h-8 text-green-500 mb-4 mx-auto" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">High Quality</h3>
              <p className="text-gray-600">Accurate, coherent, and readable summaries every time</p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div>
            <SummarizerForm onSummarize={handleSummarize} loading={loading} />
          </div>

          {/* Result */}
          <div>
            {result ? (
              <SummaryResult result={result} onExport={handleExport} />
            ) : (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="text-center py-12">
                  <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">No Summary Yet</h3>
                  <p className="text-gray-500">
                    Enter your text and click "Summarize Text" to see the results here
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2024 AI Text Summarizer. Built with Next.js and FastAPI.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
