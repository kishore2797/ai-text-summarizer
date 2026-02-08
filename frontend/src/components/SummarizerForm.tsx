'use client'

import React, { useState } from 'react'
import { Upload, FileText, Send, Download, Settings } from 'lucide-react'

interface SummarizerFormProps {
  onSummarize: (request: SummarizationRequest) => void
  loading: boolean
}

interface SummarizationRequest {
  text: string
  method: 'extractive' | 'abstractive' | 'hybrid'
  model: 'bart' | 't5' | 'pegasus' | 'openai' | 'cohere'
  max_sentences: number
  max_length: number
  min_length: number
}

export default function SummarizerForm({ onSummarize, loading }: SummarizerFormProps) {
  const [text, setText] = useState('')
  const [method, setMethod] = useState<'extractive' | 'abstractive' | 'hybrid'>('hybrid')
  const [model, setModel] = useState<'bart' | 't5' | 'pegasus' | 'openai' | 'cohere'>('bart')
  const [maxSentences, setMaxSentences] = useState(5)
  const [maxLength, setMaxLength] = useState(150)
  const [minLength, setMinLength] = useState(50)
  const [showAdvanced, setShowAdvanced] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim().length < 50) {
      alert('Please enter at least 50 characters of text to summarize.')
      return
    }

    onSummarize({
      text: text.trim(),
      method,
      model,
      max_sentences: maxSentences,
      max_length: maxLength,
      min_length: minLength
    })
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('extract_text', 'true')

    try {
      const response = await fetch('http://localhost:8000/api/v1/files/upload', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        if (result.text_extracted) {
          setText(result.text)
        }
      } else {
        alert('Failed to process file. Please try again.')
      }
    } catch (error) {
      alert('Error uploading file. Please try again.')
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">AI Text Summarizer</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Text Input Area */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Text to Summarize
          </label>
          <div className="relative">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter your text here (minimum 50 characters)..."
              className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              disabled={loading}
            />
            <div className="absolute bottom-2 right-2 text-sm text-gray-500">
              {text.length} characters
            </div>
          </div>
        </div>

        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or upload a file (PDF, DOCX, TXT)
          </label>
          <div className="flex items-center space-x-4">
            <label className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg cursor-pointer hover:bg-gray-200 transition-colors">
              <Upload className="w-4 h-4 mr-2" />
              Choose File
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileUpload}
                className="hidden"
                disabled={loading}
              />
            </label>
            <span className="text-sm text-gray-500">
              Supported formats: PDF, DOCX, TXT (max 10MB)
            </span>
          </div>
        </div>

        {/* Basic Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Summarization Method
            </label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value as any)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            >
              <option value="extractive">Extractive (Fast)</option>
              <option value="abstractive">Abstractive (High Quality)</option>
              <option value="hybrid">Hybrid (Best of Both)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value as any)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            >
              <option value="bart">BART (General Purpose)</option>
              <option value="t5">T5 (Short Text)</option>
              <option value="pegasus">PEGASUS (Long Documents)</option>
              <option value="openai">OpenAI GPT (Premium)</option>
              <option value="cohere">Cohere (Business)</option>
            </select>
          </div>
        </div>

        {/* Advanced Settings */}
        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            <Settings className="w-4 h-4 mr-2" />
            {showAdvanced ? 'Hide' : 'Show'} Advanced Settings
          </button>

          {showAdvanced && (
            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Sentences
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={maxSentences}
                  onChange={(e) => setMaxSentences(parseInt(e.target.value))}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Length (words)
                </label>
                <input
                  type="number"
                  min="50"
                  max="500"
                  value={maxLength}
                  onChange={(e) => setMaxLength(parseInt(e.target.value))}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Min Length (words)
                </label>
                <input
                  type="number"
                  min="10"
                  max="200"
                  value={minLength}
                  onChange={(e) => setMinLength(parseInt(e.target.value))}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={loading}
                />
              </div>
            </div>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || text.trim().length < 50}
          className="w-full flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Processing...
            </div>
          ) : (
            <div className="flex items-center">
              <Send className="w-4 h-4 mr-2" />
              Summarize Text
            </div>
          )}
        </button>
      </form>
    </div>
  )
}
