// Test the JavaScript trigonometric functions
const AdvancedCalculator = require('./src/utils/calculator.ts');

console.log("Testing JavaScript trigonometric functions...");

// Test expressions
const testExpressions = [
    "sin(1.5708)",  // sin(π/2) ≈ 1
    "cos(0)",       // cos(0) = 1
    "tan(0.7854)",  // tan(π/4) ≈ 1
    "Sin(1.5708)",  // Test case sensitivity
    "COS(0)",       // Test case sensitivity
    "TAN(0.7854)"   // Test case sensitivity
];

testExpressions.forEach(expr => {
    try {
        const result = AdvancedCalculator.calculate(expr);
        console.log(`${expr} = ${result}`);
    } catch (error) {
        console.log(`${expr} = Error: ${error.message}`);
    }
});

console.log("\nJavaScript trigonometric test complete.");
