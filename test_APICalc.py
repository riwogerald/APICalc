import unittest
import fractions
from APICalc import AdvancedPrecisionNumber

class TestAdvancedPrecisionNumber(unittest.TestCase):

    def test_initialization(self):
        # Test various initialization scenarios
        test_cases = [
            ("123.45", "123.45"),
            ("0b1010", "10", 2),
            ("0xFF", "255", 16),
            (42, "42.00"),
            (3.14, "3.14"),
            (fractions.Fraction(1, 3), "0.33")
        ]
        
        for input_val, expected, *base in test_cases:
            base = base[0] if base else 10
            apn = AdvancedPrecisionNumber(input_val, base=base)
            self.assertEqual(str(apn), expected)

    def test_arithmetic_operations(self):
        # Comprehensive arithmetic operation tests
        test_cases = [
            # (op, num1, num2, expected_result)
            ('add', "123.45", "876.55", "1000.00"),
            ('sub', "1000", "123.45", "876.55"),
            ('mul', "10", "5", "50.00"),
            ('div', "10", "2", "5.00"),
            ('mod', "10", "3", "1.00")
        ]
        
        for op, num1, num2, expected in test_cases:
            apn1 = AdvancedPrecisionNumber(num1)
            apn2 = AdvancedPrecisionNumber(num2)
            
            if op == 'add':
                result = apn1 + apn2
            elif op == 'sub':
                result = apn1 - apn2
            elif op == 'mul':
                result = apn1 * apn2
            elif op == 'div':
                result = apn1 / apn2
            elif op == 'mod':
                result = apn1 % apn2
            
            self.assertEqual(str(result), expected)

    def test_edge_cases(self):
        # Test edge cases and error handling
        edge_cases = [
            # (input, expected_error)
            ("invalid", ValueError),
            (float('inf'), ValueError),
            (float('nan'), ValueError)
        ]
        
        for input_val, expected_error in edge_cases:
            with self.assertRaises(expected_error):
                AdvancedPrecisionNumber(input_val)

    def test_division_scenarios(self):
        # Comprehensive division tests
        division_cases = [
            ("10", "2", "5.00"),  # Standard division
            ("1", "3", "0.33"),   # Repeating decimal
            ("-10", "2", "-5.00") # Negative number division
        ]
        
        for num1, num2, expected in division_cases:
            apn1 = AdvancedPrecisionNumber(num1)
            apn2 = AdvancedPrecisionNumber(num2)
            result = apn1 / apn2
            self.assertEqual(str(result), expected)

    def test_division_by_zero(self):
        # Specific test for division by zero
        apn1 = AdvancedPrecisionNumber("10")
        with self.assertRaises(ZeroDivisionError):
            apn1 / AdvancedPrecisionNumber("0")

    def test_advanced_operations(self):
        # Advanced mathematical operations
        advanced_cases = [
            # (method, input, expected)
            ('sqrt', "16", "4.00"),
            ('sqrt', "2", "1.41"),  # Irrational number
        ]
        
        for method, input_val, expected in advanced_cases:
            apn = AdvancedPrecisionNumber(input_val)
            if method == 'sqrt':
                result = apn.sqrt()
            self.assertEqual(str(result), expected)

    def test_fraction_conversion(self):
        # Comprehensive fraction conversion tests
        fraction_cases = [
            ("0.5", fractions.Fraction(1, 2)),
            ("0.33", fractions.Fraction(1, 3)),
            ("1.25", fractions.Fraction(5, 4))
        ]
        
        for num_str, expected_fraction in fraction_cases:
            apn = AdvancedPrecisionNumber(num_str)
            fraction = apn.as_fraction()
            self.assertEqual(fraction, expected_fraction)

if __name__ == "__main__":
    unittest.main()