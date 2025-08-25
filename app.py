#!/usr/bin/env python3
"""
Flask Web Server for Advanced Precision Calculator
Provides REST API endpoints for calculator operations
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import APICalc
import traceback
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class CalculatorAPI:
    """API handler for calculator operations"""
    
    @staticmethod
    def safe_number_creation(value, base=10, precision_mode='standard'):
        """Safely create a number, detecting if it's complex"""
        try:
            if isinstance(value, str) and ('i' in value.lower() or 'j' in value.lower()):
                return APICalc.ComplexNumber.from_string(value, base, precision_mode)
            else:
                return APICalc.AdvancedPrecisionNumber(value, base, precision_mode)
        except Exception as e:
            raise ValueError(f"Invalid number format: {value}")
    
    @staticmethod
    def format_result(result):
        """Format result for JSON serialization"""
        if isinstance(result, (APICalc.AdvancedPrecisionNumber, APICalc.ComplexNumber)):
            return str(result)
        return result

@app.route('/')
def index():
    """Serve the main calculator interface"""
    return render_template('calculator.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Main calculation endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'expression' not in data:
            return jsonify({'error': 'No expression provided'}), 400
        
        expression = data['expression'].strip()
        precision_mode = data.get('precision_mode', 'standard')
        base = data.get('base', 10)
        
        # Handle different types of calculations
        result = evaluate_expression(expression, precision_mode, base)
        
        return jsonify({
            'result': CalculatorAPI.format_result(result),
            'expression': expression,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'expression': data.get('expression', ''),
            'success': False
        }), 400

@app.route('/api/function', methods=['POST'])
def function_call():
    """Handle mathematical function calls"""
    try:
        data = request.get_json()
        
        function_name = data.get('function')
        args = data.get('args', [])
        precision_mode = data.get('precision_mode', 'standard')
        base = data.get('base', 10)
        
        if not function_name:
            return jsonify({'error': 'No function specified'}), 400
        
        # Convert arguments to appropriate number types
        processed_args = []
        for arg in args:
            processed_args.append(CalculatorAPI.safe_number_creation(arg, base, precision_mode))
        
        # Execute function
        result = execute_function(function_name, processed_args)
        
        return jsonify({
            'result': CalculatorAPI.format_result(result),
            'function': function_name,
            'args': args,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'function': data.get('function', ''),
            'success': False
        }), 400

@app.route('/api/constants', methods=['GET'])
def get_constants():
    """Get mathematical constants"""
    try:
        precision = request.args.get('precision', 25, type=int)
        precision = min(max(precision, 10), 100)  # Limit precision range
        
        pi = APICalc.AdvancedPrecisionNumber._get_pi(precision)
        e = APICalc.AdvancedPrecisionNumber._get_e(precision)
        
        return jsonify({
            'pi': str(pi),
            'e': str(e),
            'precision': precision,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@app.route('/api/convert_base', methods=['POST'])
def convert_base():
    """Convert numbers between different bases"""
    try:
        data = request.get_json()
        
        value = data.get('value')
        from_base = data.get('from_base', 10)
        to_base = data.get('to_base', 10)
        precision_mode = data.get('precision_mode', 'standard')
        
        if not value:
            return jsonify({'error': 'No value provided'}), 400
        
        # Create number in source base
        num = APICalc.AdvancedPrecisionNumber(value, from_base, precision_mode)
        
        # Convert to target base
        if to_base != from_base:
            converted = num._convert_to_base(to_base)
        else:
            converted = num
        
        return jsonify({
            'result': str(converted),
            'original_value': value,
            'from_base': from_base,
            'to_base': to_base,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

def evaluate_expression(expression, precision_mode='standard', base=10):
    """Evaluate a mathematical expression"""
    
    # Handle simple binary operations
    operators = ['+', '-', '*', '/', '**', '//', '%']
    
    for op in ['**', '//', '!=', '==', '<=', '>=']:  # Multi-character operators first
        if op in expression:
            parts = expression.split(op, 1)
            if len(parts) == 2:
                left = CalculatorAPI.safe_number_creation(parts[0].strip(), base, precision_mode)
                right = CalculatorAPI.safe_number_creation(parts[1].strip(), base, precision_mode)
                
                if op == '**':
                    return left ** right
                elif op == '//':
                    return left // right
                elif op == '!=':
                    return left != right
                elif op == '==':
                    return left == right
                elif op == '<=':
                    return left <= right
                elif op == '>=':
                    return left >= right
    
    for op in ['+', '-', '*', '/', '%', '<', '>']:
        if op in expression:
            # Handle negative numbers properly
            parts = []
            if op in ['+', '-']:
                # Split more carefully for + and -
                temp_parts = expression.split(op)
                if len(temp_parts) >= 2:
                    if op == '-' and expression.startswith('-'):
                        # Handle leading negative sign
                        if len(temp_parts) > 2:
                            parts = ['-' + temp_parts[1], op.join(temp_parts[2:])]
                        else:
                            # Just a negative number
                            return CalculatorAPI.safe_number_creation(expression, base, precision_mode)
                    else:
                        parts = [temp_parts[0], op.join(temp_parts[1:])]
            else:
                parts = expression.split(op, 1)
            
            if len(parts) == 2:
                left = CalculatorAPI.safe_number_creation(parts[0].strip(), base, precision_mode)
                right = CalculatorAPI.safe_number_creation(parts[1].strip(), base, precision_mode)
                
                if op == '+':
                    return left + right
                elif op == '-':
                    return left - right
                elif op == '*':
                    return left * right
                elif op == '/':
                    return left / right
                elif op == '%':
                    return left % right
                elif op == '<':
                    return left < right
                elif op == '>':
                    return left > right
    
    # If no operators found, try to parse as a single number
    return CalculatorAPI.safe_number_creation(expression, base, precision_mode)

def execute_function(function_name, args):
    """Execute a mathematical function"""
    
    if not args:
        raise ValueError("Function requires at least one argument")
    
    # Get the first argument (most functions are unary)
    x = args[0]
    
    # Handle functions
    if function_name == 'sin':
        return x.sin()
    elif function_name == 'cos':
        return x.cos()
    elif function_name == 'tan':
        return x.tan()
    elif function_name == 'arcsin':
        return x.arcsin()
    elif function_name == 'arccos':
        return x.arccos()
    elif function_name == 'arctan':
        return x.arctan()
    elif function_name == 'sqrt':
        return x.sqrt()
    elif function_name == 'sqr':
        return x.sqr()
    elif function_name == 'cube':
        return x.cube()
    elif function_name == 'cube_root':
        return x.cube_root()
    elif function_name == 'factorial':
        return x.factorial()
    elif function_name == 'log':
        if len(args) > 1:
            return x.log(args[1])
        else:
            return x.log()
    elif function_name == 'exp':
        return x.exp()
    elif function_name == 'abs':
        if isinstance(x, APICalc.ComplexNumber):
            return x.abs()
        else:
            return abs(x)
    elif function_name == 'conjugate':
        if isinstance(x, APICalc.ComplexNumber):
            return x.conjugate()
        else:
            return x  # Conjugate of real number is itself
    elif function_name == 'arg':
        if isinstance(x, APICalc.ComplexNumber):
            return x.arg()
        else:
            # Argument of real number
            if x.negative:
                return APICalc.AdvancedPrecisionNumber._get_pi(x.precision)
            else:
                return APICalc.AdvancedPrecisionNumber('0')
    elif function_name == 'inverse':
        return x.inverse()
    else:
        raise ValueError(f"Unknown function: {function_name}")

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Advanced Precision Calculator Web Server...")
    print("Access the calculator at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
