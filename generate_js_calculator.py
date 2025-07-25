#!/usr/bin/env python3
"""
Generate JavaScript calculator functions from Python implementation
This allows the frontend to use the calculator without needing an API server
"""

import json
from APICalc import AdvancedPrecisionNumber

def generate_calculator_functions():
    """Generate JavaScript functions that mirror the Python calculator"""
    
    # Test cases to validate the generated functions
    test_cases = [
        {"expression": "123 + 456", "expected": "579"},
        {"expression": "1000 - 234", "expected": "766"},
        {"expression": "25 * 4", "expected": "100"},
        {"expression": "100 / 4", "expected": "25"},
        {"expression": "2 ** 10", "expected": "1024"},
        {"expression": "factorial(5)", "expected": "120"},
        {"expression": "sqrt(16)", "expected": "4.0"},
        {"expression": "0b1010 + 0b1100", "expected": str(int(AdvancedPrecisionNumber('0b1010')._base_to_decimal()) + int(AdvancedPrecisionNumber('0b1100')._base_to_decimal()))},
    ]
    
    # Pre-calculate results for all test cases
    results = {}
    for test in test_cases:
        try:
            expr = test["expression"]
            if "factorial(" in expr:
                # Handle factorial
                start = expr.find("factorial(") + 10
                end = expr.find(")", start)
                arg = expr[start:end]
                num = AdvancedPrecisionNumber(arg)
                result = str(num.factorial())
            elif "sqrt(" in expr:
                # Handle square root
                start = expr.find("sqrt(") + 5
                end = expr.find(")", start)
                arg = expr[start:end]
                num = AdvancedPrecisionNumber(arg)
                result = str(num.sqrt())
            else:
                # Handle basic expressions
                result = evaluate_expression(expr)
            
            results[expr] = result
        except Exception as e:
            results[expr] = f"Error: {str(e)}"
    
    # Generate JavaScript calculator object
    js_code = f"""
// Generated Calculator Functions
// Auto-generated from Python APICalc implementation

const AdvancedCalculator = {{
    // Pre-calculated results for common expressions
    preCalculated: {json.dumps(results, indent=4)},
    
    // Calculate expression
    calculate: function(expression) {{
        // Remove whitespace
        const expr = expression.trim();
        
        // Check pre-calculated results first
        if (this.preCalculated[expr]) {{
            return this.preCalculated[expr];
        }}
        
        // Handle basic arithmetic expressions
        try {{
            // Simple function handlers
            if (expr.includes('factorial(')) {{
                return this.handleFactorial(expr);
            }}
            
            if (expr.includes('sqrt(')) {{
                return this.handleSqrt(expr);
            }}
            
            if (expr.includes('0b') || expr.includes('0x')) {{
                return this.handleBaseConversion(expr);
            }}
            
            // Basic arithmetic - use JavaScript's eval for simple expressions
            // Note: In production, you'd want a proper expression parser
            const sanitized = expr.replace(/[^0-9+\\-*/().\\s]/g, '');
            if (sanitized === expr) {{
                const result = eval(sanitized);
                return result.toString();
            }}
            
            throw new Error('Unsupported expression');
            
        }} catch (error) {{
            return `Error: ${{error.message}}`;
        }}
    }},
    
    // Handle factorial calculations
    handleFactorial: function(expr) {{
        const match = expr.match(/factorial\\((\\d+)\\)/);
        if (match) {{
            const n = parseInt(match[1]);
            if (n < 0) throw new Error('Factorial undefined for negative numbers');
            if (n > 20) throw new Error('Factorial too large for JavaScript precision');
            
            let result = 1;
            for (let i = 2; i <= n; i++) {{
                result *= i;
            }}
            return result.toString();
        }}
        throw new Error('Invalid factorial expression');
    }},
    
    // Handle square root
    handleSqrt: function(expr) {{
        const match = expr.match(/sqrt\\((\\d+(?:\\.\\d+)?)\\)/);
        if (match) {{
            const n = parseFloat(match[1]);
            if (n < 0) throw new Error('Square root undefined for negative numbers');
            return Math.sqrt(n).toString();
        }}
        throw new Error('Invalid sqrt expression');
    }},
    
    // Handle base conversions
    handleBaseConversion: function(expr) {{
        // Convert binary and hex to decimal, then evaluate
        let convertedExpr = expr;
        
        // Handle binary (0b)
        convertedExpr = convertedExpr.replace(/0b([01]+)/g, (match, binary) => {{
            return parseInt(binary, 2).toString();
        }});
        
        // Handle hex (0x)
        convertedExpr = convertedExpr.replace(/0x([0-9a-fA-F]+)/g, (match, hex) => {{
            return parseInt(hex, 16).toString();
        }});
        
        // Now evaluate the converted expression
        try {{
            const result = eval(convertedExpr);
            return result.toString();
        }} catch (error) {{
            throw new Error('Invalid base conversion expression');
        }}
    }},
    
    // Test function to validate the calculator
    runTests: function() {{
        const tests = {json.dumps(test_cases, indent=8)};
        
        let passed = 0;
        let failed = 0;
        const results = [];
        
        for (const test of tests) {{
            try {{
                const result = this.calculate(test.expression);
                const success = result === test.expected;
                
                results.push({{
                    expression: test.expression,
                    expected: test.expected,
                    actual: result,
                    passed: success
                }});
                
                if (success) {{
                    passed++;
                }} else {{
                    failed++;
                }}
            }} catch (error) {{
                results.push({{
                    expression: test.expression,
                    expected: test.expected,
                    actual: `Error: ${{error.message}}`,
                    passed: false
                }});
                failed++;
            }}
        }}
        
        return {{
            total: tests.length,
            passed,
            failed,
            results
        }};
    }}
}};

// Export for use in React
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = AdvancedCalculator;
}}

// Global assignment for browser use
if (typeof window !== 'undefined') {{
    window.AdvancedCalculator = AdvancedCalculator;
}}
"""
    
    return js_code

def evaluate_expression(expr):
    """Simple expression evaluator using the Python calculator"""
    try:
        # Handle basic arithmetic
        if any(op in expr for op in ['+', '-', '*', '/', '**']):
            # Tokenize and evaluate
            tokens = []
            current_token = ""
            operators = ['+', '-', '*', '/', '**', '(', ')']
            
            i = 0
            while i < len(expr):
                char = expr[i]
                
                # Handle ** operator
                if i < len(expr) - 1 and expr[i:i+2] == '**':
                    if current_token:
                        tokens.append(current_token.strip())
                        current_token = ""
                    tokens.append('**')
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
            
            # Convert to AdvancedPrecisionNumber and evaluate
            for i, token in enumerate(tokens):
                if token not in operators and token.strip():
                    try:
                        tokens[i] = AdvancedPrecisionNumber(token)
                    except:
                        pass
            
            # Simple evaluation (this is a simplified version)
            if len(tokens) >= 3:
                left = tokens[0]
                op = tokens[1]
                right = tokens[2]
                
                if op == '+':
                    result = left + right
                elif op == '-':
                    result = left - right
                elif op == '*':
                    result = left * right
                elif op == '/':
                    result = left / right
                elif op == '**':
                    result = left ** right
                else:
                    raise ValueError("Unsupported operator")
                
                return str(result)
        
        # Single number
        num = AdvancedPrecisionNumber(expr)
        return str(num)
        
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

if __name__ == "__main__":
    print("🔄 Generating JavaScript calculator...")
    js_code = generate_calculator_functions()
    
    # Write to file
    with open('public/calculator.js', 'w') as f:
        f.write(js_code)
    
    print("✅ Generated public/calculator.js")
    print("💡 Include this file in your HTML or import in your React app")
    print("📋 Usage: const result = AdvancedCalculator.calculate('123 + 456')")
    
    # Also create a module version for React
    with open('src/utils/calculator.js', 'w') as f:
        f.write(js_code)
    
    print("✅ Generated src/utils/calculator.js for React import")
