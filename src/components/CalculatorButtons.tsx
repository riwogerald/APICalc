import React from 'react'
import { clsx } from 'clsx'

interface CalculatorButtonsProps {
  onButtonClick: (value: string) => void
}

const CalculatorButtons: React.FC<CalculatorButtonsProps> = ({ onButtonClick }) => {
  const buttons = [
    // Row 1: Functions
    [
      { label: 'sin', value: 'sin(', type: 'function' },
      { label: 'cos', value: 'cos(', type: 'function' },
      { label: 'tan', value: 'tan(', type: 'function' },
      { label: 'log', value: 'log(', type: 'function' },
    ],
    // Row 2: More functions
    [
      { label: 'sqrt', value: 'sqrt(', type: 'function' },
      { label: 'x²', value: '**2', type: 'function' },
      { label: 'x³', value: '**3', type: 'function' },
      { label: 'n!', value: 'factorial(', type: 'function' },
    ],
    // Row 3: Numbers and operators
    [
      { label: '(', value: '(', type: 'operator' },
      { label: ')', value: ')', type: 'operator' },
      { label: 'C', value: 'C', type: 'clear' },
      { label: '⌫', value: '⌫', type: 'clear' },
    ],
    // Row 4: Numbers
    [
      { label: '7', value: '7', type: 'number' },
      { label: '8', value: '8', type: 'number' },
      { label: '9', value: '9', type: 'number' },
      { label: '/', value: '/', type: 'operator' },
    ],
    // Row 5: Numbers
    [
      { label: '4', value: '4', type: 'number' },
      { label: '5', value: '5', type: 'number' },
      { label: '6', value: '6', type: 'number' },
      { label: '*', value: '*', type: 'operator' },
    ],
    // Row 6: Numbers
    [
      { label: '1', value: '1', type: 'number' },
      { label: '2', value: '2', type: 'number' },
      { label: '3', value: '3', type: 'number' },
      { label: '-', value: '-', type: 'operator' },
    ],
    // Row 7: Numbers
    [
      { label: '0', value: '0', type: 'number' },
      { label: '.', value: '.', type: 'number' },
      { label: '**', value: '**', type: 'operator' },
      { label: '+', value: '+', type: 'operator' },
    ],
    // Row 8: Special
    [
      { label: '%', value: '%', type: 'operator' },
      { label: 'π', value: '3.14159265359', type: 'constant' },
      { label: 'e', value: '2.71828182846', type: 'constant' },
      { label: '=', value: '=', type: 'equals' },
    ],
  ]

  const getButtonClass = (type: string) => {
    return clsx(
      'calculator-button',
      {
        'operator-button': type === 'operator' || type === 'equals',
        'function-button': type === 'function',
        'bg-red-500 hover:bg-red-600 text-white border-red-500': type === 'clear',
        'bg-green-500 hover:bg-green-600 text-white border-green-500': type === 'equals',
        'bg-purple-100 hover:bg-purple-200 text-purple-700 border-purple-200': type === 'constant',
      }
    )
  }

  return (
    <div className="space-y-2">
      {buttons.map((row, rowIndex) => (
        <div key={rowIndex} className="grid grid-cols-4 gap-2">
          {row.map((button, buttonIndex) => (
            <button
              key={buttonIndex}
              onClick={() => onButtonClick(button.value)}
              className={getButtonClass(button.type)}
            >
              {button.label}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}

export default CalculatorButtons