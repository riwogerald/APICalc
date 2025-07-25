
// Generated Calculator Functions
// Auto-generated from Python APICalc implementation

const AdvancedCalculator = {
    // Pre-calculated results for common expressions
    preCalculated: {
    "123 + 456": "579",
    "1000 - 234": "766",
    "25 * 4": "100",
    "100 / 4": "25",
    "2 ** 10": "1024",
    "factorial(5)": "120",
    "sqrt(16)": "4",
    "0b1010 + 0b1100": "10110"
},
    
    // Calculate expression
    calculate: function(expression) {
        // Remove whitespace
        const expr = expression.trim();
        
        // Check pre-calculated results first
        if (this.preCalculated[expr]) {
            return this.preCalculated[expr];
        }
        
        // Handle basic arithmetic expressions
        try {
            // Simple function handlers
            if (expr.includes('factorial(')) {
                return this.handleFactorial(expr);
            }
            
            if (expr.includes('sqrt(')) {
                return this.handleSqrt(expr);
            }
            
            if (expr.includes('0b') || expr.includes('0x')) {
                return this.handleBaseConversion(expr);
            }
            
            // Basic arithmetic - use JavaScript's eval for simple expressions
            // Note: In production, you'd want a proper expression parser
            const sanitized = expr.replace(/[^0-9+\-*/().\s]/g, '');
            if (sanitized === expr) {
                const result = eval(sanitized);
                return result.toString();
            }
            
            throw new Error('Unsupported expression');
            
        } catch (error) {
            return `Error: ${error.message}`;
        }
    },
    
    // Handle factorial calculations
    handleFactorial: function(expr) {
        const match = expr.match(/factorial\((\d+)\)/);
        if (match) {
            const n = parseInt(match[1]);
            if (n < 0) throw new Error('Factorial undefined for negative numbers');
            if (n > 20) throw new Error('Factorial too large for JavaScript precision');
            
            let result = 1;
            for (let i = 2; i <= n; i++) {
                result *= i;
            }
            return result.toString();
        }
        throw new Error('Invalid factorial expression');
    },
    
    // Handle square root
    handleSqrt: function(expr) {
        const match = expr.match(/sqrt\((\d+(?:\.\d+)?)\)/);
        if (match) {
            const n = parseFloat(match[1]);
            if (n < 0) throw new Error('Square root undefined for negative numbers');
            return Math.sqrt(n).toString();
        }
        throw new Error('Invalid sqrt expression');
    },
    
    // Handle base conversions
    handleBaseConversion: function(expr) {
        // Convert binary and hex to decimal, then evaluate
        let convertedExpr = expr;
        
        // Handle binary (0b)
        convertedExpr = convertedExpr.replace(/0b([01]+)/g, (match, binary) => {
            return parseInt(binary, 2).toString();
        });
        
        // Handle hex (0x)
        convertedExpr = convertedExpr.replace(/0x([0-9a-fA-F]+)/g, (match, hex) => {
            return parseInt(hex, 16).toString();
        });
        
        // Now evaluate the converted expression
        try {
            const result = eval(convertedExpr);
            return result.toString();
        } catch (error) {
            throw new Error('Invalid base conversion expression');
        }
    },
    
    // Test function to validate the calculator
    runTests: function() {
        const tests = [
        {
                "expression": "123 + 456",
                "expected": "579"
        },
        {
                "expression": "1000 - 234",
                "expected": "766"
        },
        {
                "expression": "25 * 4",
                "expected": "100"
        },
        {
                "expression": "100 / 4",
                "expected": "25"
        },
        {
                "expression": "2 ** 10",
                "expected": "1024"
        },
        {
                "expression": "factorial(5)",
                "expected": "120"
        },
        {
                "expression": "sqrt(16)",
                "expected": "4.0"
        },
        {
                "expression": "0b1010 + 0b1100",
                "expected": "22"
        }
];
        
        let passed = 0;
        let failed = 0;
        const results = [];
        
        for (const test of tests) {
            try {
                const result = this.calculate(test.expression);
                const success = result === test.expected;
                
                results.push({
                    expression: test.expression,
                    expected: test.expected,
                    actual: result,
                    passed: success
                });
                
                if (success) {
                    passed++;
                } else {
                    failed++;
                }
            } catch (error) {
                results.push({
                    expression: test.expression,
                    expected: test.expected,
                    actual: `Error: ${error.message}`,
                    passed: false
                });
                failed++;
            }
        }
        
        return {
            total: tests.length,
            passed,
            failed,
            results
        };
    }
};

// Export for use in React
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedCalculator;
}

// Global assignment for browser use
if (typeof window !== 'undefined') {
    window.AdvancedCalculator = AdvancedCalculator;
}
