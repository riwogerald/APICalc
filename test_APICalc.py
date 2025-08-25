import unittest
import sys
import math
import fractions

# Import the module
from APICalc import AdvancedPrecisionNumber, ComplexNumber

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

class TestComplexNumber(unittest.TestCase):
    def setUp(self):
        """Set up method to create complex number instances for testing"""
        self.z1 = ComplexNumber('3', '4')  # 3+4i
        self.z2 = ComplexNumber('1', '2')  # 1+2i
        self.z_real = ComplexNumber('5', '0')  # 5+0i (real number)
        self.z_imag = ComplexNumber('0', '3')  # 0+3i (pure imaginary)
        self.z_zero = ComplexNumber('0', '0')  # 0+0i
        self.z_negative = ComplexNumber('-2', '-3')  # -2-3i

    def test_initialization_basic(self):
        """Test basic initialization of complex numbers"""
        # Test basic initialization
        z = ComplexNumber('3', '4')
        self.assertEqual(str(z), '3+4i')
        
        # Test negative imaginary part
        z_neg = ComplexNumber('3', '-4')
        self.assertEqual(str(z_neg), '3-4i')
        
        # Test zero cases
        self.assertEqual(str(self.z_zero), '0')
        self.assertEqual(str(self.z_real), '5')
        self.assertEqual(str(self.z_imag), '3i')

    def test_string_parsing(self):
        """Test parsing complex numbers from strings"""
        # Test standard format
        z1 = ComplexNumber.from_string('3+4i')
        self.assertEqual(str(z1), '3+4i')
        
        # Test negative imaginary
        z2 = ComplexNumber.from_string('3-4i')
        self.assertEqual(str(z2), '3-4i')
        
        # Test pure imaginary
        z3 = ComplexNumber.from_string('5i')
        self.assertEqual(str(z3), '5i')
        
        # Test pure real
        z4 = ComplexNumber.from_string('7')
        self.assertEqual(str(z4), '7')
        
        # Test j notation
        z5 = ComplexNumber.from_string('2+3j')
        self.assertEqual(str(z5), '2+3i')
        
        # Test unit imaginary
        z6 = ComplexNumber.from_string('i')
        self.assertEqual(str(z6), 'i')
        
        # Test negative unit imaginary
        z7 = ComplexNumber.from_string('-i')
        self.assertEqual(str(z7), '-i')

    def test_polar_form(self):
        """Test polar form creation and conversion"""
        # Create from polar coordinates
        import math
        magnitude = AdvancedPrecisionNumber('5')
        phase = AdvancedPrecisionNumber(str(math.pi/4))  # 45 degrees
        z_polar = ComplexNumber.from_polar(magnitude, phase)
        
        # Check magnitude
        self.assertAlmostEqual(float(z_polar.abs()._base_to_decimal()), 5.0, places=5)
        
        # Check that it's approximately 5*cos(pi/4) + 5*sin(pi/4)i
        expected_real = 5 * math.cos(math.pi/4)
        expected_imag = 5 * math.sin(math.pi/4)
        self.assertAlmostEqual(float(z_polar.real._base_to_decimal()), expected_real, places=5)
        self.assertAlmostEqual(float(z_polar.imag._base_to_decimal()), expected_imag, places=5)

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations with complex numbers"""
        # Addition: (3+4i) + (1+2i) = (4+6i)
        result = self.z1 + self.z2
        self.assertEqual(str(result), '4+6i')
        
        # Subtraction: (3+4i) - (1+2i) = (2+2i)
        result = self.z1 - self.z2
        self.assertEqual(str(result), '2+2i')
        
        # Multiplication: (3+4i) * (1+2i) = (3-8) + (6+4)i = -5+10i
        result = self.z1 * self.z2
        self.assertEqual(str(result), '-5+10i')
        
        # Division: (3+4i) / (1+2i)
        result = self.z1 / self.z2
        # (3+4i)/(1+2i) = (3+4i)(1-2i)/((1+2i)(1-2i)) = (3+8+4i-6i)/(1+4) = (11-2i)/5 = 2.2-0.4i
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 2.2, places=10)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), -0.4, places=10)

    def test_mixed_arithmetic(self):
        """Test arithmetic between complex and real numbers"""
        # Complex + real
        result = self.z1 + 2  # (3+4i) + 2 = (5+4i)
        self.assertEqual(str(result), '5+4i')
        
        # Real + complex
        result = 2 + self.z1  # 2 + (3+4i) = (5+4i)
        self.assertEqual(str(result), '5+4i')
        
        # Complex * real
        result = self.z1 * 2  # (3+4i) * 2 = (6+8i)
        self.assertEqual(str(result), '6+8i')
        
        # Complex / real
        result = self.z1 / 2  # (3+4i) / 2 = (1.5+2i)
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 1.5, places=10)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 2.0, places=10)

    def test_power_operations(self):
        """Test exponentiation of complex numbers"""
        # Test i^2 = -1
        i = ComplexNumber('0', '1')
        result = i ** 2
        self.assertAlmostEqual(float(result.real._base_to_decimal()), -1.0, places=10)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 0.0, places=10)
        
        # Test i^4 = 1
        result = i ** 4
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 1.0, places=5)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 0.0, places=5)
        
        # Test (1+i)^2 = 1 + 2i + i^2 = 1 + 2i - 1 = 2i
        z = ComplexNumber('1', '1')
        result = z ** 2
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 0.0, places=10)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 2.0, places=10)

    def test_conjugate(self):
        """Test complex conjugate"""
        # Conjugate of (3+4i) should be (3-4i)
        conj = self.z1.conjugate()
        self.assertEqual(str(conj), '3-4i')
        
        # Conjugate of real number should be itself
        conj_real = self.z_real.conjugate()
        self.assertEqual(str(conj_real), '5')
        
        # Conjugate of pure imaginary should flip sign
        conj_imag = self.z_imag.conjugate()
        self.assertEqual(str(conj_imag), '-3i')

    def test_magnitude_and_argument(self):
        """Test magnitude (absolute value) and argument (phase)"""
        # Magnitude of (3+4i) should be 5
        mag = self.z1.abs()
        self.assertAlmostEqual(float(mag._base_to_decimal()), 5.0, places=10)
        
        # Magnitude of real number
        mag_real = self.z_real.abs()
        self.assertAlmostEqual(float(mag_real._base_to_decimal()), 5.0, places=10)
        
        # Magnitude of pure imaginary
        mag_imag = self.z_imag.abs()
        self.assertAlmostEqual(float(mag_imag._base_to_decimal()), 3.0, places=10)
        
        # Argument of (1+i) should be pi/4
        z_45deg = ComplexNumber('1', '1')
        arg = z_45deg.arg()
        import math
        self.assertAlmostEqual(float(arg._base_to_decimal()), math.pi/4, places=5)

    def test_exponential_and_logarithm(self):
        """Test complex exponential and logarithm functions"""
        # Test Euler's identity: e^(i*pi) = -1
        import math
        i_pi = ComplexNumber('0', str(math.pi))
        result = i_pi.exp()
        self.assertAlmostEqual(float(result.real._base_to_decimal()), -1.0, places=5)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 0.0, places=5)
        
        # Test e^(i*pi/2) = i
        i_pi_half = ComplexNumber('0', str(math.pi/2))
        result = i_pi_half.exp()
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 0.0, places=5)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 1.0, places=5)
        
        # Test log(e) = 1
        e_complex = ComplexNumber(str(math.e), '0')
        result = e_complex.log()
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 1.0, places=5)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), 0.0, places=5)

    def test_square_root(self):
        """Test complex square root"""
        # Square root of -1 should be i
        neg_one = ComplexNumber('-1', '0')
        result = neg_one.sqrt()
        self.assertAlmostEqual(float(result.real._base_to_decimal()), 0.0, places=10)
        self.assertAlmostEqual(abs(float(result.imag._base_to_decimal())), 1.0, places=10)
        
        # Square root of i
        i = ComplexNumber('0', '1')
        result = i.sqrt()
        # sqrt(i) = (1+i)/sqrt(2)
        expected_val = 1.0 / math.sqrt(2)
        self.assertAlmostEqual(float(result.real._base_to_decimal()), expected_val, places=5)
        self.assertAlmostEqual(float(result.imag._base_to_decimal()), expected_val, places=5)

    def test_trigonometric_functions(self):
        """Test complex trigonometric functions"""
        # Test sin(i) = i*sinh(1)
        i = ComplexNumber('0', '1')
        sin_i = i.sin()
        import math
        expected_imag = math.sinh(1)
        self.assertAlmostEqual(float(sin_i.real._base_to_decimal()), 0.0, places=5)
        self.assertAlmostEqual(float(sin_i.imag._base_to_decimal()), expected_imag, places=5)
        
        # Test cos(i) = cosh(1)
        cos_i = i.cos()
        expected_real = math.cosh(1)
        self.assertAlmostEqual(float(cos_i.real._base_to_decimal()), expected_real, places=5)
        self.assertAlmostEqual(float(cos_i.imag._base_to_decimal()), 0.0, places=5)
        
        # Test sin(0) = 0
        zero = ComplexNumber('0', '0')
        sin_zero = zero.sin()
        self.assertAlmostEqual(float(sin_zero.real._base_to_decimal()), 0.0, places=10)
        self.assertAlmostEqual(float(sin_zero.imag._base_to_decimal()), 0.0, places=10)

    def test_utility_functions(self):
        """Test utility functions for complex numbers"""
        # Test is_real
        self.assertTrue(self.z_real.is_real())
        self.assertFalse(self.z1.is_real())
        
        # Test is_imaginary
        self.assertTrue(self.z_imag.is_imaginary())
        self.assertFalse(self.z1.is_imaginary())
        
        # Test is_zero
        self.assertTrue(self.z_zero.is_zero())
        self.assertFalse(self.z1.is_zero())
        
        # Test magnitude alias
        mag1 = self.z1.abs()
        mag2 = self.z1.magnitude()
        self.assertEqual(float(mag1._base_to_decimal()), float(mag2._base_to_decimal()))
        
        # Test phase alias
        phase1 = self.z1.arg()
        phase2 = self.z1.phase()
        self.assertEqual(float(phase1._base_to_decimal()), float(phase2._base_to_decimal()))

    def test_equality_and_comparison(self):
        """Test equality operations for complex numbers"""
        # Test equality
        z1_copy = ComplexNumber('3', '4')
        self.assertEqual(self.z1, z1_copy)
        
        # Test inequality
        self.assertNotEqual(self.z1, self.z2)
        
        # Test equality with real numbers
        real_five = ComplexNumber('5', '0')
        self.assertEqual(real_five, 5)
        
        # Test inequality with real numbers
        self.assertNotEqual(self.z1, 5)

    def test_error_handling(self):
        """Test error handling for complex numbers"""
        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            self.z1 / self.z_zero
        
        # Test argument of zero complex number
        with self.assertRaises(ValueError):
            self.z_zero.arg()
        
        # Test invalid string format
        with self.assertRaises(ValueError):
            ComplexNumber.from_string('invalid')

    def test_string_representations(self):
        """Test string representations of complex numbers"""
        # Test __str__
        self.assertIsInstance(str(self.z1), str)
        
        # Test __repr__
        self.assertIsInstance(repr(self.z1), str)
        self.assertTrue('ComplexNumber' in repr(self.z1))
        
        # Test various formats
        test_cases = [
            (ComplexNumber('0', '0'), '0'),
            (ComplexNumber('5', '0'), '5'),
            (ComplexNumber('0', '3'), '3i'),
            (ComplexNumber('0', '1'), 'i'),
            (ComplexNumber('0', '-1'), '-i'),
            (ComplexNumber('3', '4'), '3+4i'),
            (ComplexNumber('3', '-4'), '3-4i'),
        ]
        
        for complex_num, expected in test_cases:
            self.assertEqual(str(complex_num), expected)

def run_comprehensive_tests():
    """
    Run tests with a comprehensive reporting mechanism
    """
    # Prepare the test suite for both classes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases for both AdvancedPrecisionNumber and ComplexNumber
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedPrecisionNumber))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexNumber))
    
    # Create our custom result collector
    result = ImprovedTestResult()
    
    # Run the tests
    suite.run(result)
    
    # Print comprehensive test report
    print("\n" + "=" * 60)
    print("Advanced Precision Calculator Test Report")
    print("=" * 60)
    
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