import React, { useState, useEffect } from 'react'
import { Play, CheckCircle, XCircle, Clock, RefreshCw } from 'lucide-react'

interface TestCase {
  id: string
  name: string
  description: string
  expression: string
  expected: string
  category: string
}

interface TestResult {
  id: string
  passed: boolean
  actual: string
  expected: string
  duration: number
  error?: string
}

const TestPage: React.FC = () => {
  const [testCases] = useState<TestCase[]>([
    // Basic Arithmetic
    {
      id: 'add_basic',
      name: 'Basic Addition',
      description: 'Simple addition of two integers',
      expression: '123 + 456',
      expected: '579',
      category: 'Basic Arithmetic'
    },
    {
      id: 'sub_basic',
      name: 'Basic Subtraction',
      description: 'Simple subtraction of two integers',
      expression: '1000 - 234',
      expected: '766',
      category: 'Basic Arithmetic'
    },
    {
      id: 'mul_basic',
      name: 'Basic Multiplication',
      description: 'Simple multiplication of two integers',
      expression: '25 * 4',
      expected: '100',
      category: 'Basic Arithmetic'
    },
    {
      id: 'div_basic',
      name: 'Basic Division',
      description: 'Simple division of two integers',
      expression: '100 / 4',
      expected: '25',
      category: 'Basic Arithmetic'
    },
    
    // Large Numbers
    {
      id: 'large_add',
      name: 'Large Number Addition',
      description: 'Addition with very large numbers',
      expression: '123456789012345678901234567890 + 987654321098765432109876543210',
      expected: '1111111110111111111011111111100',
      category: 'Large Numbers'
    },
    {
      id: 'large_mul',
      name: 'Large Number Multiplication',
      description: 'Multiplication with large numbers',
      expression: '123456789 * 987654321',
      expected: '121932631137021795',
      category: 'Large Numbers'
    },
    
    // Advanced Functions
    {
      id: 'factorial_5',
      name: 'Factorial of 5',
      description: 'Calculate 5!',
      expression: 'factorial(5)',
      expected: '120',
      category: 'Advanced Functions'
    },
    {
      id: 'factorial_10',
      name: 'Factorial of 10',
      description: 'Calculate 10!',
      expression: 'factorial(10)',
      expected: '3628800',
      category: 'Advanced Functions'
    },
    {
      id: 'sqrt_16',
      name: 'Square Root of 16',
      description: 'Calculate √16',
      expression: 'sqrt(16)',
      expected: '4',
      category: 'Advanced Functions'
    },
    {
      id: 'power_2_10',
      name: 'Power Operation',
      description: 'Calculate 2^10',
      expression: '2 ** 10',
      expected: '1024',
      category: 'Advanced Functions'
    },
    
    // Base Conversions
    {
      id: 'binary_add',
      name: 'Binary Addition',
      description: 'Add binary numbers',
      expression: '0b1010 + 0b1100',
      expected: '0b10110',
      category: 'Base Conversions'
    },
    {
      id: 'hex_mul',
      name: 'Hexadecimal Multiplication',
      description: 'Multiply hexadecimal numbers',
      expression: '0xFF * 0x10',
      expected: '0xFF0',
      category: 'Base Conversions'
    },
    
    // Error Cases
    {
      id: 'div_zero',
      name: 'Division by Zero',
      description: 'Should handle division by zero',
      expression: '10 / 0',
      expected: 'Error: Division by zero',
      category: 'Error Handling'
    },
    {
      id: 'invalid_expr',
      name: 'Invalid Expression',
      description: 'Should handle invalid syntax',
      expression: '10 + + 5',
      expected: 'Error: Invalid expression',
      category: 'Error Handling'
    }
  ])

  const [testResults, setTestResults] = useState<TestResult[]>([])
  const [isRunning, setIsRunning] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const [runningTestId, setRunningTestId] = useState<string | null>(null)

  const categories = ['All', ...Array.from(new Set(testCases.map(test => test.category)))]

  const filteredTests = selectedCategory === 'All' 
    ? testCases 
    : testCases.filter(test => test.category === selectedCategory)

  const runSingleTest = async (testCase: TestCase): Promise<TestResult> => {
    const startTime = Date.now()
    setRunningTestId(testCase.id)
    
    try {
      // Simulate API call to Python backend
      await new Promise(resolve => setTimeout(resolve, Math.random() * 500 + 200))
      
      // Mock calculation result (in real app, this would call your Python backend)
      const actual = await mockCalculation(testCase.expression)
      const duration = Date.now() - startTime
      
      return {
        id: testCase.id,
        passed: actual === testCase.expected,
        actual,
        expected: testCase.expected,
        duration
      }
    } catch (error) {
      const duration = Date.now() - startTime
      return {
        id: testCase.id,
        passed: false,
        actual: '',
        expected: testCase.expected,
        duration,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    } finally {
      setRunningTestId(null)
    }
  }

  const mockCalculation = async (expression: string): Promise<string> => {
    // Mock implementation - in real app, this would call your Python backend
    if (expression.includes('/ 0')) {
      return 'Error: Division by zero'
    }
    if (expression.includes('+ +')) {
      return 'Error: Invalid expression'
    }
    if (expression === 'factorial(5)') return '120'
    if (expression === 'factorial(10)') return '3628800'
    if (expression === 'sqrt(16)') return '4'
    if (expression === '2 ** 10') return '1024'
    if (expression === '123 + 456') return '579'
    if (expression === '1000 - 234') return '766'
    if (expression === '25 * 4') return '100'
    if (expression === '100 / 4') return '25'
    
    // For other expressions, try basic evaluation
    try {
      const sanitized = expression.replace(/[^0-9+\-*/().\s]/g, '')
      if (sanitized === expression) {
        return eval(sanitized).toString()
      }
    } catch (error) {
      // Ignore
    }
    
    return 'Mock result'
  }

  const runAllTests = async () => {
    setIsRunning(true)
    setTestResults([])
    
    const results: TestResult[] = []
    
    for (const testCase of filteredTests) {
      const result = await runSingleTest(testCase)
      results.push(result)
      setTestResults([...results])
    }
    
    setIsRunning(false)
  }

  const runSingleTestHandler = async (testCase: TestCase) => {
    const result = await runSingleTest(testCase)
    setTestResults(prev => {
      const filtered = prev.filter(r => r.id !== testCase.id)
      return [...filtered, result]
    })
  }

  const getTestResult = (testId: string) => {
    return testResults.find(result => result.id === testId)
  }

  const passedTests = testResults.filter(r => r.passed).length
  const totalTests = testResults.length

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Test Suite Interface
          </h1>
          <p className="text-gray-600">
            Comprehensive testing for the Advanced Precision Calculator
          </p>
        </div>

        {/* Test Controls */}
        <div className="card mb-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={runAllTests}
                disabled={isRunning}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                {isRunning ? (
                  <div className="spinner" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
                <span>{isRunning ? 'Running Tests...' : 'Run All Tests'}</span>
              </button>
              
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="input-field w-auto"
                disabled={isRunning}
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>

            {totalTests > 0 && (
              <div className="flex items-center space-x-4 text-sm">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>{passedTests} passed</span>
                </div>
                <div className="flex items-center space-x-2">
                  <XCircle className="w-4 h-4 text-red-600" />
                  <span>{totalTests - passedTests} failed</span>
                </div>
                <div className="text-gray-600">
                  {totalTests} / {filteredTests.length} tests run
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Test Results Summary */}
        {totalTests > 0 && (
          <div className="card mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Test Results</h2>
              <div className="text-sm text-gray-600">
                Success Rate: {totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0}%
              </div>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${totalTests > 0 ? (passedTests / totalTests) * 100 : 0}%` }}
              />
            </div>
          </div>
        )}

        {/* Test Cases */}
        <div className="space-y-4">
          {filteredTests.map((testCase) => {
            const result = getTestResult(testCase.id)
            const isCurrentlyRunning = runningTestId === testCase.id

            return (
              <div key={testCase.id} className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {testCase.name}
                      </h3>
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                        {testCase.category}
                      </span>
                      
                      {result && (
                        <div className="flex items-center space-x-2">
                          {result.passed ? (
                            <CheckCircle className="w-5 h-5 text-green-600" />
                          ) : (
                            <XCircle className="w-5 h-5 text-red-600" />
                          )}
                          <span className="text-sm text-gray-500">
                            {result.duration}ms
                          </span>
                        </div>
                      )}
                      
                      {isCurrentlyRunning && (
                        <div className="flex items-center space-x-2">
                          <div className="spinner" />
                          <span className="text-sm text-gray-500">Running...</span>
                        </div>
                      )}
                    </div>
                    
                    <p className="text-gray-600 mb-3">{testCase.description}</p>
                    
                    <div className="space-y-2">
                      <div>
                        <span className="text-sm font-medium text-gray-700">Expression:</span>
                        <code className="ml-2 bg-gray-100 px-2 py-1 rounded text-sm font-mono">
                          {testCase.expression}
                        </code>
                      </div>
                      
                      <div>
                        <span className="text-sm font-medium text-gray-700">Expected:</span>
                        <code className="ml-2 bg-gray-100 px-2 py-1 rounded text-sm font-mono">
                          {testCase.expected}
                        </code>
                      </div>
                      
                      {result && (
                        <div>
                          <span className="text-sm font-medium text-gray-700">Actual:</span>
                          <code className={`ml-2 px-2 py-1 rounded text-sm font-mono ${
                            result.passed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {result.actual || result.error}
                          </code>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <button
                    onClick={() => runSingleTestHandler(testCase)}
                    disabled={isRunning || isCurrentlyRunning}
                    className="btn-secondary ml-4 disabled:opacity-50"
                  >
                    {isCurrentlyRunning ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <Play className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        {filteredTests.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">No tests found for the selected category.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default TestPage