import unittest
import sys
import fractions
import warnings

# Ensure the path includes the directory with the original module (Remember to change this to the path where you saved APICalc.py)
sys.path.append('D:\Files\Codex\Github\PesaPal\APICalc\APICalc.py')
from APICalc import AdvancedPrecisionNumber

class TestAdvancedPrecisionNumber(unittest.TestCase):
    def setUp(self):
        """Set up method to create instances for testing"""
        self.a = AdvancedPrecisionNumber('10.5')
        self.b = AdvancedPrecisionNumber('3.2')
        self.zero = AdvancedPrecisionNumber('0')
        self.one = AdvancedPrecisionNumber('1')
        self.negative = AdvancedPrecisionNumber('-5.5')

    def test_initialization(self):
        """Test various initialization methods"""
        # Standard decimal initialization
        self.assertEqual(str(AdvancedPrecisionNumber('10.5')), '10.5')
        
        # Binary, octal, hex initialization
        self.assertEqual(str(AdvancedPrecisionNumber('0b1010')), '0b1010')
        self.assertEqual(str(AdvancedPrecisionNumber('0o12')), '0o12')
        self.assertEqual(str(AdvancedPrecisionNumber('0x0A')), '0x10')
        
        # Negative number initialization
        self.assertEqual(str(AdvancedPrecisionNumber('-10.5')), '-10.5')
        
        # Fraction initialization
        frac = AdvancedPrecisionNumber(fraction='1/2')
        self.assertEqual(str(frac), '0.5 (Fraction: 1/2)')

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        # Addition
        self.assertEqual(str(self.a + self.b), '13.7')
        self.assertEqual(str(self.a + 3), '13.5')
        
        # Subtraction
        self.assertEqual(str(self.a - self.b), '7.3')
        self.assertEqual(str(self.a - 3), '7.5')
        
        # Multiplication
        self.assertEqual(str(self.a * self.b), '33.6')
        self.assertEqual(str(self.a * 3), '31.5')
        
        # Division
        self.assertEqual(str(self.a / self.b), '3.28125')
        self.assertEqual(str(self.a / 2), '5.25')
        
        # Modulo
        self.assertEqual(str(self.a % self.b), '1.1')

    def test_comparison_operations(self):
        """Test comparison methods"""
        self.assertTrue(self.a > self.b)
        self.assertTrue(self.a >= self.b)
        self.assertFalse(self.a < self.b)
        self.assertFalse(self.a == self.b)
        
        self.assertTrue(self.zero == 0)
        self.assertTrue(self.one > 0)
        self.assertTrue(self.negative < 0)

    def test_unary_operations(self):
        """Test unary operations"""
        # Absolute value
        self.assertEqual(str(abs(self.negative)), '5.5')
        
        # Exponentiation
        self.assertEqual(str(self.a ** 2), '110.25')
        
        # Square root
        sqrt_a = self.a.sqrt()
        self.assertAlmostEqual(sqrt_a._base_to_decimal(), 3.2403703, places=6)
        
        # Cube and cube root
        cube_a = self.a.cube()
        self.assertEqual(str(cube_a), '1157.625')
        cube_root_a = self.a.cube_root()
        self.assertAlmostEqual(cube_root_a._base_to_decimal(), 2.214, places=3)

    def test_trigonometric_functions(self):
        """Test trigonometric functions"""
        # Sine of 1 radian
        sin_val = self.one.sin()
        self.assertAlmostEqual(sin_val._base_to_decimal(), 0.8414709848, places=6)
        
        # Cosine of 1 radian
        cos_val = self.one.cos()
        self.assertAlmostEqual(cos_val._base_to_decimal(), 0.5403023058, places=6)
        
        # Tangent of 1 radian
        tan_val = self.one.tan()
        self.assertAlmostEqual(tan_val._base_to_decimal(), 1.5574077246, places=6)

    def test_inverse_trigonometric_functions(self):
        """Test inverse trigonometric functions"""
        # Arcsine tests
        half = AdvancedPrecisionNumber('0.5')
        arcsin_val = half.arcsin()
        self.assertAlmostEqual(arcsin_val._base_to_decimal(), 0.5235987755, places=6)
        
        # Arccosine tests
        arccos_val = half.arccos()
        self.assertAlmostEqual(arccos_val._base_to_decimal(), 1.0471975511, places=6)
        
        # Arctangent tests
        arctan_val = self.one.arctan()
        self.assertAlmostEqual(arctan_val._base_to_decimal(), 0.7853981633, places=6)

    def test_logarithmic_functions(self):
        """Test logarithmic functions"""
        # Natural logarithm
        ln_a = self.a.log()
        self.assertAlmostEqual(ln_a._base_to_decimal(), 2.3513752571, places=6)
        
        # Logarithm with base 2
        base_2 = AdvancedPrecisionNumber('2')
        log2_a = self.a.log(base_2)
        self.assertAlmostEqual(log2_a._base_to_decimal(), 3.3903989439, places=6)

    def test_fraction_conversion(self):
        """Test fraction conversion methods"""
        # To fraction
        frac_a = self.a.to_fraction()
        self.assertEqual(frac_a, fractions.Fraction(21, 2))
        
        # Fraction from initialization
        frac_num = AdvancedPrecisionNumber(fraction='3/4')
        self.assertEqual(str(frac_num), '0.75 (Fraction: 3/4)')

    def test_error_handling(self):
        """Test error handling for various operations"""
        # Division by zero
        with self.assertRaises(ZeroDivisionError):
            self.one / self.zero
        
        # Square root of negative number
        with self.assertRaises(ValueError):
            self.negative.sqrt()
        
        # Factorial of non-integer
        with self.assertRaises(ValueError):
            self.a.factorial()
        
        # Logarithm of non-positive number
        with self.assertRaises(ValueError):
            self.negative.log()
        
        # Arcsine/Arccosine out of domain
        with self.assertRaises(ValueError):
            AdvancedPrecisionNumber('2').arcsin()
        
        with self.assertRaises(ValueError):
            AdvancedPrecisionNumber('2').arccos()

    def test_edge_cases(self):
        """Test various edge cases"""
        # Handling very small numbers
        small = AdvancedPrecisionNumber('1e-10')
        self.assertIsNotNone(small)
        
        # Large number handling
        large = AdvancedPrecisionNumber('1e100')
        self.assertIsNotNone(large)
        
        # Multiple base conversions
        binary = AdvancedPrecisionNumber('0b1010')
        hex_num = AdvancedPrecisionNumber('0xA')
        self.assertEqual(binary._base_to_decimal(), hex_num._base_to_decimal())

def run_tests():
    """Run all tests and print results"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvancedPrecisionNumber)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    run_tests()