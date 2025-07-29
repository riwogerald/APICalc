// Python Calculator Integration using Pyodide
// This allows running the actual Python APICalc code directly in the browser

declare global {
  interface Window {
    loadPyodide: any;
    pyodide: any;
  }
}

interface PyodideInterface {
  runPython: (code: string) => any;
  loadPackage: (packages: string | string[]) => Promise<void>;
  globals: {
    get: (name: string) => any;
    set: (name: string, value: any) => void;
  };
}

class PythonCalculatorEngine {
  private pyodide: PyodideInterface | null = null;
  private initialized = false;
  private initPromise: Promise<void> | null = null;

  async initialize(): Promise<void> {
    if (this.initialized) return;
    if (this.initPromise) return this.initPromise;

    this.initPromise = this._doInitialize();
    return this.initPromise;
  }

  private async _doInitialize(): Promise<void> {
    try {
      // Load Pyodide
      if (!window.loadPyodide) {
        // Dynamically load Pyodide
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js';
        document.head.appendChild(script);
        
        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
        });
      }

      this.pyodide = await window.loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
      });

      // Install required packages
      await this.pyodide.loadPackage(['micropip']);
      
      // Install our Python calculator code
      await this.installCalculatorCode();
      
      this.initialized = true;
      console.log('🐍 Python calculator engine initialized successfully!');
    } catch (error) {
      console.error('Failed to initialize Python calculator:', error);
      throw error;
    }
  }

  private async installCalculatorCode(): Promise<void> {
    if (!this.pyodide) throw new Error('Pyodide not initialized');

    const pythonCode = `
import fractions
import math
import re
from decimal import Decimal, getcontext

# Set high precision
getcontext().prec = 50

class AdvancedPrecisionNumber:
    def __init__(self, value='0', base=10):
        self.base = base
        self.negative = False
        self.value = Decimal('0')
        
        if isinstance(value, str):
            self._parse_string(value)
        else:
            self.value = Decimal(str(value))
    
    def _parse_string(self, value):
        value = value.strip()
        self.negative = value.startswith('-')
        value = value.lstrip('-+')
        
        # Base detection
        if value.lower().startswith('0b'):
            self.base = 2
            self.value = Decimal(int(value[2:], 2))
        elif value.lower().startswith('0x'):
            self.base = 16
            self.value = Decimal(int(value[2:], 16))
        elif value.lower().startswith('0o'):
            self.base = 8
            self.value = Decimal(int(value[2:], 8))
        else:
            self.value = Decimal(value)
        
        if self.negative:
            self.value = -self.value
    
    def __add__(self, other):
        if isinstance(other, AdvancedPrecisionNumber):
            return AdvancedPrecisionNumber(str(self.value + other.value))
        return AdvancedPrecisionNumber(str(self.value + Decimal(str(other))))
    
    def __sub__(self, other):
        if isinstance(other, AdvancedPrecisionNumber):
            return AdvancedPrecisionNumber(str(self.value - other.value))
        return AdvancedPrecisionNumber(str(self.value - Decimal(str(other))))
    
    def __mul__(self, other):
        if isinstance(other, AdvancedPrecisionNumber):
            return AdvancedPrecisionNumber(str(self.value * other.value))
        return AdvancedPrecisionNumber(str(self.value * Decimal(str(other))))
    
    def __truediv__(self, other):
        other_val = other.value if isinstance(other, AdvancedPrecisionNumber) else Decimal(str(other))
        if other_val == 0:
            raise ZeroDivisionError("Division by zero")
        return AdvancedPrecisionNumber(str(self.value / other_val))
    
    def __pow__(self, other):
        other_val = other.value if isinstance(other, AdvancedPrecisionNumber) else Decimal(str(other))
        return AdvancedPrecisionNumber(str(self.value ** other_val))
    
    def factorial(self):
        if self.value < 0 or self.value != int(self.value):
            raise ValueError("Factorial only defined for non-negative integers")
        
        n = int(self.value)
        result = 1
        for i in range(2, n + 1):
            result *= i
        return AdvancedPrecisionNumber(str(result))
    
    def sqrt(self):
        if self.value < 0:
            raise ValueError("Square root of negative number")
        return AdvancedPrecisionNumber(str(self.value.sqrt()))
    
    def sin(self):
        return AdvancedPrecisionNumber(str(math.sin(float(self.value))))
    
    def cos(self):
        return AdvancedPrecisionNumber(str(math.cos(float(self.value))))
    
    def tan(self):
        return AdvancedPrecisionNumber(str(math.tan(float(self.value))))
    
    def log(self, base=None):
        if self.value <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        if base:
            base_val = base.value if isinstance(base, AdvancedPrecisionNumber) else Decimal(str(base))
            return AdvancedPrecisionNumber(str(math.log(float(self.value), float(base_val))))
        return AdvancedPrecisionNumber(str(math.log(float(self.value))))
    
    def __str__(self):
        # Format based on original base for display
        if self.base == 2 and self.value == int(self.value):
            return f"0b{bin(int(self.value))[2:]}"
        elif self.base == 16 and self.value == int(self.value):
            return f"0x{hex(int(self.value))[2:].upper()}"
        elif self.base == 8 and self.value == int(self.value):
            return f"0o{oct(int(self.value))[2:]}"
        else:
            # Format nicely for large integers
            if self.value == int(self.value):
                return str(int(self.value))
            else:
                return str(self.value)

def safe_calculate(expression):
    """Safely evaluate mathematical expressions"""
    try:
        # Handle function calls
        if any(func in expression for func in ['factorial(', 'sqrt(', 'sin(', 'cos(', 'tan(', 'log(']):
            return handle_function_call(expression)
        
        # Handle simple expressions using tokenization
        tokens = safe_eval(expression)
        result = evaluate_expression(tokens)
        return str(result)
        
    except Exception as e:
        return f"Error: {str(e)}"

def handle_function_call(expression):
    """Handle function calls like factorial(5), sqrt(16), etc."""
    for func_name in ['factorial', 'sqrt', 'sqr', 'cube', 'cube_root', 'inverse', 
                      'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'log', 'exp']:
        if f'{func_name}(' in expression:
            start = expression.find(f'{func_name}(') + len(func_name) + 1
            end = expression.find(')', start)
            if end != -1:
                arg = expression[start:end].strip()
                
                # Handle log with base
                if func_name == 'log' and ',' in arg:
                    args = [a.strip() for a in arg.split(',')]
                    num = AdvancedPrecisionNumber(args[0])
                    base = AdvancedPrecisionNumber(args[1])
                    result = num.log(base)
                else:
                    num = AdvancedPrecisionNumber(arg)
                    result = getattr(num, func_name)()
                
                return str(result)
    
    raise ValueError("Unknown function")

def safe_eval(expr):
    """Safely tokenize mathematical expressions"""
    tokens = []
    current_token = ""
    operators = ['+', '-', '*', '/', '%', '(', ')', '**', '//', '!']
    
    i = 0
    while i < len(expr):
        char = expr[i]
        
        # Handle multi-character operators
        if i < len(expr) - 1:
            two_char = expr[i:i+2]
            if two_char in ['**', '//']:
                if current_token:
                    tokens.append(current_token.strip())
                    current_token = ""
                tokens.append(two_char)
                i += 2
                continue
        
        if char in operators:
            if current_token:
                tokens.append(current_token.strip())
                current_token = ""
            tokens.append(char)
        else:
            current_token += char
        
        i += 1
    
    if current_token:
        tokens.append(current_token.strip())
    
    # Convert numeric tokens to AdvancedPrecisionNumber
    for i, token in enumerate(tokens):
        if token not in operators and token.strip():
            try:
                tokens[i] = AdvancedPrecisionNumber(token)
            except:
                pass
    
    return tokens

def evaluate_expression(tokens):
    """Evaluate tokenized expression with proper operator precedence"""
    if len(tokens) == 1:
        return tokens[0]
    
    # Handle factorial first
    i = 0
    while i < len(tokens):
        if tokens[i] == '!':
            if i > 0:
                result = tokens[i-1].factorial()
                tokens = tokens[:i-1] + [result] + tokens[i+1:]
                i -= 1
            else:
                raise ValueError("Invalid factorial usage")
        i += 1
    
    # Handle exponentiation (right-to-left)
    i = len(tokens) - 1
    while i >= 0:
        if tokens[i] == '**':
            if i > 0 and i < len(tokens) - 1:
                result = tokens[i-1] ** tokens[i+1]
                tokens = tokens[:i-1] + [result] + tokens[i+2:]
                i -= 2
            else:
                raise ValueError("Invalid exponentiation")
        i -= 1
    
    # Handle multiplication, division, modulo (left-to-right)
    i = 0
    while i < len(tokens):
        if tokens[i] in ['*', '/', '//', '%']:
            if i > 0 and i < len(tokens) - 1:
                if tokens[i] == '*':
                    result = tokens[i-1] * tokens[i+1]
                elif tokens[i] == '/':
                    result = tokens[i-1] / tokens[i+1]
                elif tokens[i] == '//':
                    result = tokens[i-1] // tokens[i+1]
                elif tokens[i] == '%':
                    result = tokens[i-1] % tokens[i+1]
                
                tokens = tokens[:i-1] + [result] + tokens[i+2:]
                i -= 1
            else:
                raise ValueError(f"Invalid {tokens[i]} operation")
        i += 1
    
    # Handle addition and subtraction (left-to-right)
    i = 0
    while i < len(tokens):
        if tokens[i] in ['+', '-']:
            if i > 0 and i < len(tokens) - 1:
                if tokens[i] == '+':
                    result = tokens[i-1] + tokens[i+1]
                elif tokens[i] == '-':
                    result = tokens[i-1] - tokens[i+1]
                
                tokens = tokens[:i-1] + [result] + tokens[i+2:]
                i -= 1
            else:
                raise ValueError(f"Invalid {tokens[i]} operation")
        i += 1
    
    if len(tokens) == 1:
        return tokens[0]
    else:
        raise ValueError("Could not evaluate expression")

# Export the main calculation function
calculate = safe_calculate
    `;

    this.pyodide.runPython(pythonCode);
  }

  async calculate(expression: string): Promise<string> {
    if (!this.initialized) {
      await this.initialize();
    }

    if (!this.pyodide) {
      throw new Error('Python calculator not initialized');
    }

    try {
      // Set the expression in Python
      this.pyodide.globals.set('user_expression', expression);
      
      // Run the calculation
      const result = this.pyodide.runPython(`
try:
    result = calculate(user_expression)
    result
except Exception as e:
    f"Error: {str(e)}"
      `);

      return String(result);
    } catch (error) {
      return `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
    }
  }

  isInitialized(): boolean {
    return this.initialized;
  }
}

// Singleton instance
const pythonCalculator = new PythonCalculatorEngine();

export default pythonCalculator;
