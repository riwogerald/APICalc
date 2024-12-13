import unittest
import sys
import fractions
import warnings
import math
import random
from decimal import Decimal

# Ensure the path includes the directory with the original module (Remember to change this to the path where you saved APICalc.py)
sys.path.append('D:\Files\Codex\Github\PesaPal\APICalc\APICalc.py')
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

    def test_initialization_extended(self):
        """Extended initialization tests"""
        # Test various numeric formats
        self.assertEqual(str(AdvancedPrecisionNumber('1.23e-5')), '0.0000123')
        self.assertEqual(str(AdvancedPrecisionNumber('1.23E+5')), '123000.0')
        
        # Test string representations
        self.assertEqual(str(AdvancedPrecisionNumber(' 10.5 ')), '10.5')  # Whitespace
        self.assertEqual(str(AdvancedPrecisionNumber('+10.5')), '10.5')   # Explicit positive
        
        # Test different bases with various cases
        self.assertEqual(str(AdvancedPrecisionNumber('0B1010')), '0b1010')  # Binary uppercase
        self.assertEqual(str(AdvancedPrecisionNumber('0o12')), '0o12')      # Octal
        self.assertEqual(str(AdvancedPrecisionNumber('0XFF')), '0xff')      # Hex uppercase

        # Test fraction strings
        self.assertEqual(str(AdvancedPrecisionNumber(fraction='22/7')), '3.142857142857143 (Fraction: 22/7)')
        
        # Test invalid inputs
        with self.assertRaises(ValueError):
            AdvancedPrecisionNumber('abc')
        with self.assertRaises(ValueError):
            AdvancedPrecisionNumber('1.2.3')

    def test_arithmetic_extended(self):
        """Extended arithmetic operation tests"""
        # Chain operations
        result = self.a + self.b * self.one - self.zero
        self.assertEqual(str(result), '13.7')
        
        # Mixed operations with different types
        self.assertEqual(str(self.a + 3.5), '14.0')
        self.assertEqual(str(self.a + Decimal('3.5')), '14.0')
        self.assertEqual(str(self.a + fractions.Fraction(7, 2)), '14.0')
        
        # Operation with zero
        self.assertEqual(str(self.a + self.zero), str(self.a))
        self.assertEqual(str(self.a * self.zero), '0')
        
        # Operation with one
        self.assertEqual(str(self.a * self.one), str(self.a))
        self.assertEqual(str(self.a / self.one), str(self.a))

    def test_advanced_math_operations(self):
        """Test advanced mathematical operations"""
        # Power operations
        self.assertEqual(str(self.a ** 0), '1')
        self.assertEqual(str(self.a ** 1), str(self.a))
        self.assertEqual(str(self.a ** -1), str(1/float(self.a)))
        
        # Root operations
        cube = self.a ** 3
        self.assertAlmostEqual(float(cube.cube_root()), float(self.a), places=10)
        
        # Factorial for integers
        five = AdvancedPrecisionNumber('5')
        self.assertEqual(str(five.factorial()), '120')

    def test_trigonometric_extended(self):
        """Extended trigonometric function tests"""
        # Test at special angles
        zero_sin = self.zero.sin()
        self.assertAlmostEqual(float(zero_sin), 0, places=10)
        
        pi_half = self.pi / 2
        cos_pi_half = pi_half.cos()
        self.assertAlmostEqual(float(cos_pi_half), 0, places=10)
        
        # Test inverse functions
        for val in [-1, -0.5, 0, 0.5, 1]:
            x = AdvancedPrecisionNumber(str(val))
            # Test asin(sin(x)) = x for values in domain
            if -1 <= val <= 1:
                self.assertAlmostEqual(
                    float(x.sin().arcsin()),
                    val,
                    places=10
                )

    def test_logarithmic_extended(self):
        """Extended logarithmic function tests"""
        # Test log properties
        # log(a*b) = log(a) + log(b)
        log_product = (self.a * self.b).log()
        log_sum = self.a.log() + self.b.log()
        self.assertAlmostEqual(float(log_product), float(log_sum), places=10)
        
        # Test with different bases
        base_2 = AdvancedPrecisionNumber('2')
        base_10 = AdvancedPrecisionNumber('10')
        self.assertAlmostEqual(
            float(self.a.log(base_2)),
            math.log2(float(self.a)),
            places=10
        )

    def test_precision_and_rounding(self):
        """Test precision handling and rounding behavior"""
        # Test with high precision numbers
        high_precision = AdvancedPrecisionNumber('1.23456789012345')
        self.assertGreaterEqual(len(str(high_precision).split('.')[1]), 14)
        
        # Test rounding behavior
        result = self.a / 3
        self.assertTrue(len(str(result).split('.')[1]) <= 15)

    def test_special_values(self):
        """Test handling of special values"""
        # Test infinity handling
        with self.assertRaises(OverflowError):
            AdvancedPrecisionNumber('1e1000')
        
        # Test very small numbers
        small = AdvancedPrecisionNumber('1e-300')
        self.assertNotEqual(float(small), 0)

    def test_string_representation(self):
        """Test string representation methods"""
        # Test __str__ and __repr__
        self.assertIsInstance(str(self.a), str)
        self.assertIsInstance(repr(self.a), str)
        
        # Test format method
        self.assertEqual(format(self.a, '.2f'), '10.50')
        self.assertEqual(format(self.a, '.0f'), '11')

    def test_comparison_extended(self):
        """Extended comparison tests"""
        numbers = [self.zero, self.one, self.a, self.b, self.negative]
        # Test transitivity
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] < numbers[j]:
                    self.assertTrue(numbers[i] <= numbers[j])
                    self.assertFalse(numbers[i] > numbers[j])
                    self.assertFalse(numbers[i] >= numbers[j])

    def test_hash_and_equality(self):
        """Test hash consistency and equality"""
        # Same value should have same hash
        a1 = AdvancedPrecisionNumber('10.5')
        a2 = AdvancedPrecisionNumber('10.5')
        self.assertEqual(hash(a1), hash(a2))
        
        # Different values should have different hashes
        self.assertNotEqual(hash(self.a), hash(self.b))

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
    
    for result_type in result.detailed_results:
        if len(result_type) == 2:
            # Success case
            print(f"{result_type[0]} {result_type[1]}")
        else:
            # Failure or error case
            print(f"{result_type[0]} {result_type[1]}")
            print(f"Details: {result_type[2]}")
    
    # Final status
    if result.test_details['failed'] == 0 and result.test_details['errors'] == 0:
        print("\nAll Tests Passed Successfully!")
    else:
        print("\nSome Tests Failed. Please Review.")
    
    return result

def main():
    """Main entry point for running tests"""
    # Run the tests
    run_comprehensive_tests()

if __name__ == '__main__':
    main()