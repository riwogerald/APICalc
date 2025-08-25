import React, { useState, useRef, useEffect } from 'react'
import { Send, History, Trash2, Copy, Check, Wifi, WifiOff } from 'lucide-react'
import CalculatorButtons from '../components/CalculatorButtons'
import calculatorApi from '../services/calculatorApi'
import localCalculator from '../utils/calculator'

interface HistoryEntry {
  expression: string
  result: string
  timestamp: Date
}

const CalculatorPage: React.FC = () => {
  const [input, setInput] = useState('')
  const [result, setResult] = useState('')
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const [isApiMode, setIsApiMode] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // Check API availability on component mount
    const checkApiStatus = async () => {
      const available = await calculatorApi.checkApiHealth()
      setIsApiMode(available)
    }
    checkApiStatus()

    // Load history from localStorage
    const savedHistory = localStorage.getItem('calculator-history')
    if (savedHistory) {
      try {
        const parsed = JSON.parse(savedHistory)
        setHistory(parsed.map((entry: any) => ({
          ...entry,
          timestamp: new Date(entry.timestamp)
        })))
      } catch (error) {
        console.error('Failed to load history:', error)
      }
    }
  }, [])

  useEffect(() => {
    // Save history to localStorage
    localStorage.setItem('calculator-history', JSON.stringify(history))
  }, [history])

  const handleCalculate = async () => {
    if (!input.trim()) return

    setIsLoading(true)
    try {
      const calculationResult = await performCalculation(input)
      setResult(calculationResult)
      
      // Add to history
      const newEntry: HistoryEntry = {
        expression: input,
        result: calculationResult,
        timestamp: new Date()
      }
      
      setHistory(prev => [newEntry, ...prev.slice(0, 49)]) // Keep last 50 entries
      
    } catch (error) {
      setResult(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsLoading(false)
    }
  }

  const performCalculation = async (expression: string): Promise<string> => {
    try {
      // First try Python API for arbitrary precision
      const apiResult = await calculatorApi.calculate(expression)
      console.log('🐍 Using Python API for calculation')
      return apiResult
    } catch (apiError) {
      console.warn('Python API failed, falling back to local calculator:', apiError)
      setIsApiMode(false) // Update API status
      
      try {
        // Fallback to local TypeScript calculator
        const result = localCalculator.calculate(expression)
        
        // Check if result is an error
        if (typeof result === 'string' && result.startsWith('Error:')) {
          throw new Error(result.substring(7)) // Remove 'Error: ' prefix
        }
        
        console.log('📱 Using local TypeScript calculator')
        return result
      } catch (localError) {
        if (localError instanceof Error) {
          throw localError
        }
        throw new Error('Both API and local calculation failed')
      }
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleCalculate()
    }
  }

  const handleButtonClick = (value: string) => {
    if (value === '=') {
      handleCalculate()
    } else if (value === 'C') {
      setInput('')
      setResult('')
    } else if (value === '⌫') {
      setInput(prev => prev.slice(0, -1))
    } else {
      setInput(prev => prev + value)
      if (inputRef.current) {
        inputRef.current.focus()
      }
    }
  }

  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('calculator-history')
  }

  const copyToClipboard = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }

  const useHistoryEntry = (entry: HistoryEntry) => {
    setInput(entry.expression)
    setResult(entry.result)
    setShowHistory(false)
  }

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Advanced Precision Calculator
          </h1>
          <p className="text-gray-600 mb-4">
            Enter mathematical expressions with arbitrary precision
          </p>
          
          {/* API Status Indicator */}
          <div className="inline-flex items-center space-x-2 px-3 py-2 rounded-lg text-sm bg-gray-50">
            {isApiMode ? (
              <>
                <Wifi className="w-4 h-4 text-green-600" />
                <span className="text-green-600 font-medium">Python API Connected</span>
                <span className="text-gray-500">(Arbitrary Precision)</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-orange-600" />
                <span className="text-orange-600 font-medium">Local Calculator</span>
                <span className="text-gray-500">(Limited Precision)</span>
              </>
            )}
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Calculator Interface */}
          <div className="lg:col-span-2">
            <div className="card">
              {/* Display */}
              <div className="mb-6">
                <div className="bg-gray-50 rounded-xl p-4 mb-4">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Enter expression (e.g., 123 + 456, factorial(10), sqrt(16))"
                    className="w-full bg-transparent text-lg font-mono focus:outline-none"
                  />
                </div>
                
                {result && (
                  <div className="bg-primary-50 border border-primary-200 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-primary-600 font-medium">Result:</span>
                      <button
                        onClick={() => copyToClipboard(result, -1)}
                        className="text-primary-600 hover:text-primary-700 p-1"
                        title="Copy result"
                      >
                        {copiedIndex === -1 ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                      </button>
                    </div>
                    <div className="text-xl font-mono text-primary-900 mt-1 break-all">
                      {result}
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 mb-6">
                <button
                  onClick={handleCalculate}
                  disabled={!input.trim() || isLoading}
                  className="btn-primary flex items-center space-x-2 flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="spinner" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                  <span>{isLoading ? 'Calculating...' : 'Calculate'}</span>
                </button>
                
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <History className="w-4 h-4" />
                  <span>History</span>
                </button>
              </div>

              {/* Calculator Buttons */}
              <CalculatorButtons onButtonClick={handleButtonClick} />
            </div>
          </div>

          {/* History Panel */}
          <div className="lg:col-span-1">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">History</h3>
                {history.length > 0 && (
                  <button
                    onClick={clearHistory}
                    className="text-red-600 hover:text-red-700 p-1"
                    title="Clear history"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>

              <div className="space-y-3 max-h-96 overflow-y-auto">
                {history.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    No calculations yet
                  </p>
                ) : (
                  history.map((entry, index) => (
                    <div
                      key={index}
                      className="bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors cursor-pointer"
                      onClick={() => useHistoryEntry(entry)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-mono text-gray-700 truncate">
                            {entry.expression}
                          </div>
                          <div className="text-sm font-mono text-primary-600 truncate">
                            = {entry.result}
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            {entry.timestamp.toLocaleTimeString()}
                          </div>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            copyToClipboard(entry.result, index)
                          }}
                          className="text-gray-400 hover:text-gray-600 p-1 ml-2"
                          title="Copy result"
                        >
                          {copiedIndex === index ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Quick Reference */}
            <div className="card mt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Reference</h3>
              <div className="space-y-2 text-sm">
                <div><code className="bg-gray-100 px-2 py-1 rounded">+, -, *, /</code> Basic operations</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">**</code> Exponentiation</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">%</code> Modulo</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">factorial(n)</code> Factorial</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">sqrt(n)</code> Square root</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">log(n)</code> Logarithm</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">0b1010</code> Binary</div>
                <div><code className="bg-gray-100 px-2 py-1 rounded">0xFF</code> Hexadecimal</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CalculatorPage