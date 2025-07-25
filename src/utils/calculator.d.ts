// TypeScript declarations for calculator.js module

export interface TestCase {
  expression: string;
  expected: string;
  actual: string;
  passed: boolean;
}

export interface TestResults {
  total: number;
  passed: number;
  failed: number;
  results: TestCase[];
}

export interface AdvancedCalculatorInterface {
  /**
   * Pre-calculated results for common expressions
   */
  preCalculated: Record<string, string>;

  /**
   * Calculate a mathematical expression
   * @param expression - The mathematical expression to evaluate
   * @returns The calculated result as a string
   */
  calculate(expression: string): string;

  /**
   * Handle factorial calculations
   * @param expr - Expression containing factorial function
   * @returns The factorial result as a string
   */
  handleFactorial(expr: string): string;

  /**
   * Handle square root calculations
   * @param expr - Expression containing sqrt function
   * @returns The square root result as a string
   */
  handleSqrt(expr: string): string;

  /**
   * Handle base conversion calculations
   * @param expr - Expression containing binary/hex numbers
   * @returns The converted result as a string
   */
  handleBaseConversion(expr: string): string;

  /**
   * Run all test cases
   * @returns Test results summary
   */
  runTests(): TestResults;
}

declare const AdvancedCalculator: AdvancedCalculatorInterface;
export default AdvancedCalculator;
