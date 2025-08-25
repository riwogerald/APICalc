#!/usr/bin/env python3
"""
API Server for Advanced Precision Calculator
Exposes calculator functionality via REST API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import json
import time
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
            if any(func in expression.lower() for func in ['factorial(', 'sqrt(', 'sin(', 'cos(', 'tan(', 'log(']):
                return self.handle_function_call(expression)
            
            # Handle power operator (**)
            if '**' in expression:
                return self.handle_binary_operation(expression, '**')
            
            # Handle other binary operations
            for op in ['*', '/', '+', '-']:
                if op in expression:
                    return self.handle_binary_operation(expression, op)
            
            # Handle simple numbers or base conversions
            try:
                num = AdvancedPrecisionNumber(expression)
                return str(num)
            except:
                # Last resort: try eval for basic arithmetic
                if all(c in '0123456789+-*/.()\t\n ' for c in expression):
                    result = eval(expression)
                    return str(result)
                else:
                    raise ValueError(f"Unsupported expression: {expression}")
            
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def handle_binary_operation(self, expression, operator):
        """Handle binary operations like +, -, *, /, **"""
        parts = expression.split(operator, 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid {operator} operation")
        
        left_str = parts[0].strip()
        right_str = parts[1].strip()
        
        # Convert to AdvancedPrecisionNumber
        left = AdvancedPrecisionNumber(left_str)
        right = AdvancedPrecisionNumber(right_str)
        
        # Perform operation
        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            result = left / right
        elif operator == '**':
            result = left ** right
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return str(result)
    
    def handle_function_call(self, expression):
        """Handle function calls like factorial(5), sqrt(16), etc."""
        for func_name in ['factorial', 'sqrt', 'sqr', 'cube', 'cube_root', 'inverse', 
                          'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'log', 'exp']:
            if f'{func_name}(' in expression.lower():
                start = expression.lower().find(f'{func_name}(') + len(func_name) + 1
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
