#!/usr/bin/env python3
"""
API Server for Advanced Precision Calculator
Exposes calculator functionality via REST API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import json
from APICalc import AdvancedPrecisionNumber

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

class CalculatorAPI:
    def __init__(self):
        self.history = []
    
    def safe_calculate(self, expression):
        """Safely evaluate mathematical expressions"""
        try:
            # Handle function calls
            if any(func in expression for func in ['factorial(', 'sqrt(', 'sin(', 'cos(', 'tan(', 'log(']):
                return self.handle_function_call(expression)
            
            # Handle simple expressions using existing logic from REPL
            tokens = self.safe_eval(expression)
            result = self.evaluate_expression(tokens)
            return str(result)
            
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def handle_function_call(self, expression):
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
    
    def safe_eval(self, expr):
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
    
    def evaluate_expression(self, tokens):
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

# Create calculator instance
calculator = CalculatorAPI()

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate mathematical expression"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()
        
        if not expression:
            return jsonify({'error': 'No expression provided'}), 400
        
        result = calculator.safe_calculate(expression)
        
        # Add to history
        history_entry = {
            'expression': expression,
            'result': result,
            'timestamp': str(int(time.time() * 1000))  # JavaScript timestamp
        }
        calculator.history.insert(0, history_entry)
        calculator.history = calculator.history[:50]  # Keep last 50
        
        return jsonify({
            'result': result,
            'expression': expression,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get calculation history"""
    return jsonify({
        'history': calculator.history,
        'success': True
    })

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear calculation history"""
    calculator.history.clear()
    return jsonify({
        'message': 'History cleared',
        'success': True
    })

@app.route('/api/test', methods=['POST'])
def run_test():
    """Run a single test case"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        expected = data.get('expected', '')
        
        start_time = time.time()
        result = calculator.safe_calculate(expression)
        duration = int((time.time() - start_time) * 1000)  # milliseconds
        
        passed = str(result) == expected
        
        return jsonify({
            'passed': passed,
            'actual': str(result),
            'expected': expected,
            'duration': duration,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'passed': False,
            'actual': '',
            'expected': expected,
            'duration': 0,
            'error': str(e),
            'success': False
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Advanced Precision Calculator API is running'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    import time
    print("🚀 Starting Advanced Precision Calculator API Server...")
    print("📊 API Endpoints:")
    print("   POST /api/calculate - Calculate expression")
    print("   GET  /api/history   - Get calculation history")
    print("   DELETE /api/history - Clear history")
    print("   POST /api/test      - Run test case")
    print("   GET  /api/health    - Health check")
    print("🌐 Server will run on http://localhost:5000")
    print("🔗 Frontend should connect to this URL")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
