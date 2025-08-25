#!/usr/bin/env python3
"""
Test script to verify the REPL functionality with complex numbers
"""

import APICalc
import sys

def test_repl_operations():
    """Test various REPL operations programmatically"""
    
    print("Testing REPL operations...")
    
    # Test basic complex number creation and parsing
    test_cases = [
        # Format: (input_string, description)
        ('3+4i', 'Basic complex number'),
        ('5-2i', 'Complex with negative imaginary'),
        ('-3+7i', 'Negative real, positive imaginary'),
        ('-2-5i', 'Both negative'),
        ('8i', 'Pure imaginary positive'),
        ('-6i', 'Pure imaginary negative'),
        ('42', 'Pure real number'),
        ('0+0i', 'Zero complex number'),
    ]
    
    print("\n--- Complex Number Parsing Tests ---")
    for test_input, description in test_cases:
        try:
            if 'i' in test_input or 'j' in test_input:
                result = APICalc.ComplexNumber.from_string(test_input)
            else:
                result = APICalc.AdvancedPrecisionNumber(test_input)
            print(f"✓ {description:30} | {test_input:10} -> {result}")
        except Exception as e:
            print(f"✗ {description:30} | {test_input:10} -> ERROR: {e}")
    
    # Test arithmetic operations
    print("\n--- Complex Arithmetic Tests ---")
    try:
        c1 = APICalc.ComplexNumber.from_string('3+4i')
        c2 = APICalc.ComplexNumber.from_string('2-5i')
        
        operations = [
            (c1 + c2, 'Addition'),
            (c1 - c2, 'Subtraction'), 
            (c1 * c2, 'Multiplication'),
            (c1 / c2, 'Division'),
            (c1.conjugate(), 'Conjugate'),
            (c1.abs(), 'Magnitude'),
        ]
        
        print(f"c1 = {c1}")
        print(f"c2 = {c2}")
        
        for result, operation in operations:
            print(f"✓ {operation:15} -> {result}")
            
    except Exception as e:
        print(f"✗ Arithmetic error: {e}")
    
    # Test trigonometric functions
    print("\n--- Trigonometric Function Tests ---")
    try:
        x = APICalc.AdvancedPrecisionNumber('1.0')
        c = APICalc.ComplexNumber.from_string('1+1i')
        
        trig_tests = [
            (x.sin(), 'sin(1.0)'),
            (x.cos(), 'cos(1.0)'),
            (x.arctan(), 'arctan(1.0)'),
            (c.sin(), 'sin(1+1i)'),
            (c.cos(), 'cos(1+1i)'),
        ]
        
        for result, test_name in trig_tests:
            print(f"✓ {test_name:15} -> {result}")
            
    except Exception as e:
        print(f"✗ Trigonometric error: {e}")
    
    print("\n--- Mathematical Constants Tests ---")
    try:
        pi = APICalc.AdvancedPrecisionNumber._get_pi(15)
        e = APICalc.AdvancedPrecisionNumber._get_e(15)
        print(f"✓ Pi (15 digits)  -> {pi}")
        print(f"✓ e (15 digits)   -> {e}")
    except Exception as e:
        print(f"✗ Constants error: {e}")
    
    print("\n=== All REPL operation tests completed ===")

if __name__ == "__main__":
    test_repl_operations()
