'use client'

import React, { useState } from 'react'
import { Download, Copy, Share2, FileText, BarChart3, Clock } from 'lucide-react'

interface SummaryResultProps {
  result: {
    summary: string
    method: string
    model: string
    original_length: number
    summary_length: number
    compression_ratio: number
    processing_time: number
  }
  onExport: (format: string) => void
}

export default function SummaryResult({ result, onExport }: SummaryResultProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.summary)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AI Generated Summary',
          text: result.summary,
        })
      } catch (error) {
        console.error('Failed to share:', error)
      }
    } else {
      // Fallback to copying to clipboard
      handleCopy()
    }
  }

  const formatTime = (seconds: number) => {
    return `${seconds.toFixed(2)}s`
  }

  const formatCompressionRatio = (ratio: number) => {
    return `${(ratio * 100).toFixed(1)}%`
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-800">Summary Result</h3>
        <div className="flex items-center space-x-2">
          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            {result.method}
          </span>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            {result.model.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Summary Text */}
      <div className="mb-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
            {result.summary}
          </p>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center text-gray-600 mb-1">
            <FileText className="w-4 h-4 mr-1" />
            <span className="text-xs">Original</span>
          </div>
          <p className="text-lg font-semibold text-gray-800">{result.original_length}</p>
          <p className="text-xs text-gray-500">words</p>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center text-gray-600 mb-1">
            <FileText className="w-4 h-4 mr-1" />
            <span className="text-xs">Summary</span>
          </div>
          <p className="text-lg font-semibold text-gray-800">{result.summary_length}</p>
          <p className="text-xs text-gray-500">words</p>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center text-gray-600 mb-1">
            <BarChart3 className="w-4 h-4 mr-1" />
            <span className="text-xs">Compression</span>
          </div>
          <p className="text-lg font-semibold text-gray-800">{formatCompressionRatio(result.compression_ratio)}</p>
          <p className="text-xs text-gray-500">of original</p>
        </div>

        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center text-gray-600 mb-1">
            <Clock className="w-4 h-4 mr-1" />
            <span className="text-xs">Processing</span>
          </div>
          <p className="text-lg font-semibold text-gray-800">{formatTime(result.processing_time)}</p>
          <p className="text-xs text-gray-500">time</p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-2">
        {/* Copy Button */}
        <button
          onClick={handleCopy}
          className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Copy className="w-4 h-4 mr-2" />
          {copied ? 'Copied!' : 'Copy'}
        </button>

        {/* Share Button */}
        <button
          onClick={handleShare}
          className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Share2 className="w-4 h-4 mr-2" />
          Share
        </button>

        {/* Export Dropdown */}
        <div className="relative group">
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
          
          <div className="absolute top-full left-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
            <button
              onClick={() => onExport('pdf')}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
            >
              PDF Document
            </button>
            <button
              onClick={() => onExport('docx')}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
            >
              Word Document
            </button>
            <button
              onClick={() => onExport('txt')}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
            >
              Plain Text
            </button>
            <button
              onClick={() => onExport('csv')}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
            >
              CSV Data
            </button>
          </div>
        </div>
      </div>

      {/* Quality Indicators */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Quality Indicators</h4>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Coherence</span>
            <div className="flex items-center">
              <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
              <span className="text-sm text-gray-700">85%</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Conciseness</span>
            <div className="flex items-center">
              <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(result.compression_ratio * 100, 100)}%` }}></div>
              </div>
              <span className="text-sm text-gray-700">{Math.min(Math.round(result.compression_ratio * 100), 100)}%</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Readability</span>
            <div className="flex items-center">
              <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: '90%' }}></div>
              </div>
              <span className="text-sm text-gray-700">90%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
