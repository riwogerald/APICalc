#!/usr/bin/env python
"""Simple test script for complex number support"""

from APICalc import ComplexNumber, AdvancedPrecisionNumber

def test_complex_basics():
    print("Testing complex number basic operations...")
    
    # Test basic creation
    try:
        z1 = ComplexNumber('3', '4')
        print(f"✓ Created complex number: {z1}")
        
        z2 = ComplexNumber.from_string('2+5i')
        print(f"✓ Parsed from string: {z2}")
        
        # Test basic arithmetic
        z3 = z1 + z2
        print(f"✓ Addition: {z1} + {z2} = {z3}")
        
        z4 = z1 * z2
        print(f"✓ Multiplication: {z1} * {z2} = {z4}")
        
        # Test conjugate
        z5 = z1.conjugate()
        print(f"✓ Conjugate: conjugate({z1}) = {z5}")
        
        # Test magnitude
        mag = z1.abs()
        print(f"✓ Magnitude: |{z1}| = {mag}")
        
        print("✓ All basic complex operations successful!")
        return True
        
    except Exception as e:
        print(f"✗ Error in complex operations: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_trig():
    print("\nTesting complex trigonometric functions...")
    
    try:
        z = ComplexNumber('1', '1')  # 1+i
        print(f"Testing with z = {z}")
        
        sin_z = z.sin()
        print(f"✓ sin({z}) = {sin_z}")
        
        cos_z = z.cos()
        print(f"✓ cos({z}) = {cos_z}")
        
        print("✓ Complex trigonometric functions successful!")
        return True
        
    except Exception as e:
        print(f"✗ Error in complex trig functions: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_repl_integration():
    print("\nTesting REPL integration...")
    
    try:
        # Test real number operations
        num1 = AdvancedPrecisionNumber('5')
        result1 = num1.sin()
        print(f"✓ Real sin(5) = {result1}")
        
        # Test if complex number parsing works in REPL context
        from APICalc import calculate_repl
        print("✓ REPL imports successfully")
        
        print("✓ REPL integration successful!")
        return True
        
    except Exception as e:
        print(f"✗ Error in REPL integration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running Complex Number Support Tests")
    print("=" * 50)
    
    results = []
    results.append(test_complex_basics())
    results.append(test_complex_trig())
    results.append(test_repl_integration())
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Complex number support is working.")
    else:
        print("✗ Some tests failed. Complex number support needs fixes.")
    
    print("=" * 50)
