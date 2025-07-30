import unittest
import sys
import math
import fractions

# Import the module
from APICalc import AdvancedPrecisionNumber

class ImprovedTestResult(unittest.TestResult):
    """
    Custom test result class to provide more detailed output
    """
    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1):
        super().__init__(stream, descriptions, verbosity)
        self.test_details = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0
        }
        self.detailed_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_details['total'] += 1
        self.test_details['passed'] += 1
        self.detailed_results.append((
            "PASS",
            str(test)
        ))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_details['total'] += 1
        self.test_details['failed'] += 1
        self.detailed_results.append((
            "FAIL",
            str(test),
            self._exc_info_to_string(err, test)
        ))

    def addError(self, test, err):
        super().addError(test, err)
        self.test_details['total'] += 1
        self.test_details['errors'] += 1
        self.detailed_results.append((
            "ERROR",
            str(test),
            self._exc_info_to_string(err, test)
        ))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_details['total'] += 1
        self.test_details['skipped'] += 1
        self.detailed_results.append((
            "SKIP",
            str(test),
            reason
        ))

    def test_large_number_operations(self):
        """Test operations with very large numbers"""
        # Test large addition
        large1 = AdvancedPrecisionNumber('123456789012345678901234567890')
        large2 = AdvancedPrecisionNumber('987654321098765432109876543210')
        result = large1 + large2
        expected = '1111111110111111111011111111100'
        self.assertEqual(str(result._base_to_decimal()), expected)
        
        # Test large multiplication
        num1 = AdvancedPrecisionNumber('123456789')
        num2 = AdvancedPrecisionNumber('987654321')
        result = num1 * num2
        expected = '121932631137021795'
        # Convert result to string and check
        result_str = str(int(float(result._base_to_decimal())))
        self.assertEqual(result_str, expected)
        
        # Test factorial of larger number
        ten = AdvancedPrecisionNumber('10')
        result = ten.factorial()
        expected = 3628800
        self.assertEqual(int(result._base_to_decimal()), expected)

    def test_binary_hex_operations(self):
        """Test binary and hexadecimal operations"""
        # Binary operations
        bin1 = AdvancedPrecisionNumber('0b1010')  # 10 in decimal
        bin2 = AdvancedPrecisionNumber('0b1100')  # 12 in decimal
        
        # Test binary addition
        result = bin1 + bin2
        expected_decimal = 10 + 12  # 22
        self.assertEqual(int(result._base_to_decimal()), expected_decimal)
        
        # Hexadecimal operations
        hex1 = AdvancedPrecisionNumber('0xFF')    # 255 in decimal
        hex2 = AdvancedPrecisionNumber('0x10')    # 16 in decimal
        
        # Test hex multiplication
        result = hex1 * hex2
        expected_decimal = 255 * 16  # 4080
        self.assertEqual(int(result._base_to_decimal()), expected_decimal)
        
        # Test mixed base operations
        result = bin1 + hex2  # 10 + 16 = 26
        self.assertEqual(int(result._base_to_decimal()), 26)

class TestAdvancedPrecisionNumber(unittest.TestCase):
    def setUp(self):
        """Set up method to create instances for testing"""
        self.a = AdvancedPrecisionNumber('10.5')
        self.b = AdvancedPrecisionNumber('3.2')
        self.zero = AdvancedPrecisionNumber('0')
        self.one = AdvancedPrecisionNumber('1')
        self.negative = AdvancedPrecisionNumber('-5.5')
        self.pi = AdvancedPrecisionNumber(str(math.pi))
        self.e = AdvancedPrecisionNumber(str(math.e))

    def test_initialization_basic(self):
        """Test basic initialization"""
        # Test integer initialization
        num1 = AdvancedPrecisionNumber('42')
        self.assertEqual(str(num1), '42')
        
        # Test float initialization
        num2 = AdvancedPrecisionNumber('3.14159')
        self.assertTrue('3.14159' in str(num2))
        
        # Test negative numbers
        num3 = AdvancedPrecisionNumber('-123')
        self.assertEqual(str(num3), '-123')

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        # Addition
        result = self.a + self.b
        self.assertAlmostEqual(float(result._base_to_decimal()), 13.7, places=10)
        
        # Subtraction
        result = self.a - self.b
        self.assertAlmostEqual(float(result._base_to_decimal()), 7.3, places=10)
        
        # Multiplication
        result = self.a * self.b
        self.assertAlmostEqual(float(result._base_to_decimal()), 33.6, places=10)
        
        # Division
        result = self.a / self.b
        self.assertAlmostEqual(float(result._base_to_decimal()), 10.5/3.2, places=10)

    def test_base_conversion(self):
        """Test different number bases"""
        # Binary
        binary = AdvancedPrecisionNumber('0b1010')
        self.assertEqual(binary.base, 2)
        
        # Hexadecimal
        hex_num = AdvancedPrecisionNumber('0xFF')
        self.assertEqual(hex_num.base, 16)
        
        # Octal
        octal = AdvancedPrecisionNumber('0o17')
        self.assertEqual(octal.base, 8)

    def test_factorial(self):
        """Test factorial operation"""
        five = AdvancedPrecisionNumber('5')
        result = five.factorial()
        self.assertEqual(int(result._base_to_decimal()), 120)
        
        # Test factorial of 0
        zero_fact = self.zero.factorial()
        self.assertEqual(int(zero_fact._base_to_decimal()), 1)

    def test_power_operations(self):
        """Test exponentiation"""
        base = AdvancedPrecisionNumber('2')
        result = base ** 3
        self.assertEqual(int(result._base_to_decimal()), 8)
        
        # Test power of 0
        result = base ** 0
        self.assertEqual(int(result._base_to_decimal()), 1)

    def test_square_root(self):
        """Test square root"""
        nine = AdvancedPrecisionNumber('9')
        result = nine.sqrt()
        self.assertAlmostEqual(float(result._base_to_decimal()), 3.0, places=10)

    def test_modulo(self):
        """Test modulo operation"""
        ten = AdvancedPrecisionNumber('10')
        three = AdvancedPrecisionNumber('3')
        result = ten % three
        self.assertEqual(int(result._base_to_decimal()), 1)

    def test_comparison_operations(self):
        """Test comparison operations"""
        self.assertTrue(self.a > self.b)
        self.assertTrue(self.b < self.a)
        self.assertTrue(self.a >= self.b)
        self.assertTrue(self.b <= self.a)
        self.assertFalse(self.a == self.b)
        self.assertTrue(self.a != self.b)

    def test_trigonometric_functions(self):
        """Test trigonometric functions"""
        # Test sin(pi/2) = 1
        pi_half = AdvancedPrecisionNumber(str(math.pi / 2))
        sin_pi_half = pi_half.sin()
        self.assertAlmostEqual(float(sin_pi_half._base_to_decimal()), 1, places=5)
        
        # Test cos(0) = 1
        cos_zero = self.zero.cos()
        self.assertAlmostEqual(float(cos_zero._base_to_decimal()), 1, places=10)
        
        # Test tan(pi/4) = 1
        pi_quarter = AdvancedPrecisionNumber(str(math.pi / 4))
        tan_pi_quarter = pi_quarter.tan()
        self.assertAlmostEqual(float(tan_pi_quarter._base_to_decimal()), 1, places=5)

    def test_logarithm(self):
        """Test logarithm function"""
        e_num = AdvancedPrecisionNumber(str(math.e))
        result = e_num.log()
        self.assertAlmostEqual(float(result._base_to_decimal()), 1.0, places=5)

    def test_fraction_conversion(self):
        """Test fraction conversion"""
        half = AdvancedPrecisionNumber('0.5')
        frac = half.to_fraction()
        self.assertEqual(frac, fractions.Fraction(1, 2))

    def test_error_handling(self):
        """Test error handling"""
        # Division by zero
        with self.assertRaises(ZeroDivisionError):
            self.a / self.zero
        
        # Square root of negative number
        with self.assertRaises(ValueError):
            self.negative.sqrt()
        
        # Factorial of negative number
        with self.assertRaises(ValueError):
            self.negative.factorial()

    def test_string_representation(self):
        """Test string representation"""
        num = AdvancedPrecisionNumber('123.456')
        self.assertIsInstance(str(num), str)
        self.assertIsInstance(repr(num), str)

    def test_hash_functionality(self):
        """Test hash functionality"""
        num1 = AdvancedPrecisionNumber('10.5')
        num2 = AdvancedPrecisionNumber('10.5')
        self.assertEqual(hash(num1), hash(num2))

def run_comprehensive_tests():
    """
    Run tests with a comprehensive reporting mechanism
    """
    # Prepare the test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvancedPrecisionNumber)
    
    # Create our custom result collector
    result = ImprovedTestResult()
    
    # Run the tests
    suite.run(result)
    
    # Print comprehensive test report
    print("\n" + "=" * 50)
    print("Advanced Precision Number Test Report")
    print("=" * 50)
    
    # Print summary statistics
    print("\nTest Summary:")
    print(f"Total Tests:  {result.test_details['total']}")
    print(f"Passed:       {result.test_details['passed']}")
    print(f"Failed:       {result.test_details['failed']}")
    print(f"Errors:       {result.test_details['errors']}")
    print(f"Skipped:      {result.test_details['skipped']}")
    
    # Print detailed results
    print("\n" + "=" * 50)
    print("Detailed Test Results:")
    print("=" * 50)
    
    for result_item in result.detailed_results:
        if len(result_item) == 2:
            # Success case
            print(f"{result_item[0]:6} {result_item[1]}")
        else:
            # Failure or error case
            print(f"{result_item[0]:6} {result_item[1]}")
            if len(result_item) > 2:
                print(f"       Details: {result_item[2][:100]}...")
    
    # Final status
    if result.test_details['failed'] == 0 and result.test_details['errors'] == 0:
        print("\n✅ All Tests Passed Successfully!")
    else:
        print(f"\n❌ {result.test_details['failed'] + result.test_details['errors']} Tests Failed. Please Review.")
    
    return result

def main():
    """Main entry point for running tests"""
    print("Running Advanced Precision Number Tests...")
    run_comprehensive_tests()

if __name__ == '__main__':
    main()