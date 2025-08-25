#!/usr/bin/env python3
"""
Calculator CLI Wrapper
Simple command-line interface for the Advanced Precision Calculator
Allows local execution without needing a server
"""

import sys
import json
import argparse
from APICalc import AdvancedPrecisionNumber

class CalculatorCLI:
    def __init__(self, precision_mode='standard'):
        self.precision_mode = precision_mode
    
    def safe_calculate(self, expression):
        """Safely evaluate mathematical expressions (same logic as API server)"""
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
                num = AdvancedPrecisionNumber(expression, precision_mode=self.precision_mode)
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
        left = AdvancedPrecisionNumber(left_str, precision_mode=self.precision_mode)
        right = AdvancedPrecisionNumber(right_str, precision_mode=self.precision_mode)
        
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
                        num = AdvancedPrecisionNumber(args[0], precision_mode=self.precision_mode)
                        base = AdvancedPrecisionNumber(args[1], precision_mode=self.precision_mode)
                        result = num.log(base)
                    else:
                        num = AdvancedPrecisionNumber(arg, precision_mode=self.precision_mode)
                        result = getattr(num, func_name)()
                    
                    return str(result)
        
        raise ValueError("Unknown function")

def calculate_expression(expression, precision_mode='standard'):
    """Calculate a mathematical expression and return JSON result"""
    try:
        calc = CalculatorCLI(precision_mode=precision_mode)
        result = calc.safe_calculate(expression)
        
        return {
            "success": True,
            "result": str(result),
            "expression": expression,
            "precision_mode": precision_mode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression,
            "precision_mode": precision_mode
        }

def run_test(expression, expected):
    """Run a test case and return JSON result"""
    try:
        calc_result = calculate_expression(expression)
        
        if not calc_result["success"]:
            return {
                "success": False,
                "passed": False,
                "actual": "",
                "expected": expected,
                "error": calc_result["error"]
            }
        
        actual = calc_result["result"]
        passed = actual == expected
        
        return {
            "success": True,
            "passed": passed,
            "actual": actual,
            "expected": expected,
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "passed": False,
            "actual": "",
            "expected": expected,
            "error": str(e)
        }

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Advanced Precision Calculator CLI')
    parser.add_argument('--calculate', '-c', type=str, help='Calculate mathematical expression')
    parser.add_argument('--test', '-t', nargs=2, metavar=('EXPRESSION', 'EXPECTED'), 
                       help='Test expression against expected result')
    parser.add_argument('--precision', '-p', type=str, default='standard',
                       choices=['standard', 'high', 'extreme'],
                       help='Precision mode (default: standard)')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--version', '-v', action='store_true', help='Show version information')
    
    args = parser.parse_args()
    
    if args.version:
        print("Advanced Precision Calculator CLI v1.0.0")
        print("Python-based arbitrary precision calculator")
        return
    
    if args.calculate:
        result = calculate_expression(args.calculate, args.precision)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"{args.calculate} = {result['result']}")
            else:
                print(f"Error: {result['error']}")
                sys.exit(1)
    
    elif args.test:
        expression, expected = args.test
        result = run_test(expression, expected)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                status = "PASS" if result["passed"] else "FAIL"
                print(f"[{status}] {expression}")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {result['actual']}")
            else:
                print(f"[ERROR] {expression}")
                print(f"  Error: {result['error']}")
                sys.exit(1)
    
    else:
        # Interactive mode
        print("Advanced Precision Calculator - Interactive Mode")
        print("Enter mathematical expressions (type 'quit' to exit):")
        print("Available precision modes: standard, high, extreme")
        print("Set precision with: precision <mode>")
        print()
        
        precision_mode = 'standard'
        
        while True:
            try:
                user_input = input(f"calc[{precision_mode}]> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if user_input.startswith('precision '):
                    new_precision = user_input.split(' ', 1)[1].strip()
                    if new_precision in ['standard', 'high', 'extreme']:
                        precision_mode = new_precision
                        print(f"Precision mode set to: {precision_mode}")
                    else:
                        print("Invalid precision mode. Available: standard, high, extreme")
                    continue
                
                if user_input:
                    result = calculate_expression(user_input, precision_mode)
                    if result["success"]:
                        print(f"= {result['result']}")
                    else:
                        print(f"Error: {result['error']}")
                
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
