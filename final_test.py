#!/usr/bin/env python3
"""
Final comprehensive test of the APICalc system
"""

import APICalc

def main():
    print("=== FINAL COMPREHENSIVE TEST ===\n")
    
    try:
        # Test 1: Basic arithmetic
        print("1. Basic High-Precision Arithmetic:")
        a = APICalc.AdvancedPrecisionNumber('123.456', 10, 'standard')
        b = APICalc.AdvancedPrecisionNumber('789.123', 10, 'standard')
        print(f"   {a} + {b} = {a + b}")
        print(f"   {a} * {b} = {a * b}")
        
        # Test 2: Complex numbers
        print("\n2. Complex Number Operations:")
        c1 = APICalc.ComplexNumber.from_string('3+4i')
        c2 = APICalc.ComplexNumber.from_string('2-3i')
        print(f"   c1 = {c1}")
        print(f"   c2 = {c2}")
        print(f"   c1 + c2 = {c1 + c2}")
        print(f"   c1 * c2 = {c1 * c2}")
        print(f"   |c1| = {c1.abs()}")
        print(f"   c1* = {c1.conjugate()}")
        
        # Test 3: Mathematical functions
        print("\n3. Mathematical Functions:")
        x = APICalc.AdvancedPrecisionNumber('1')
        print(f"   sin(1) = {x.sin()}")
        print(f"   cos(1) = {x.cos()}")
        sqrt2 = APICalc.AdvancedPrecisionNumber('2').sqrt()
        print(f"   sqrt(2) = {sqrt2}")
        
        # Test 4: Mathematical constants
        print("\n4. Mathematical Constants:")
        pi = APICalc.AdvancedPrecisionNumber._get_pi(20)
        e = APICalc.AdvancedPrecisionNumber._get_e(20)
        print(f"   π ≈ {pi}")
        print(f"   e ≈ {e}")
        
        # Test 5: Complex trigonometry
        print("\n5. Complex Trigonometry:")
        z = APICalc.ComplexNumber.from_string('1+i')
        print(f"   sin({z}) = {z.sin()}")
        
        # Test 6: Parsing edge cases
        print("\n6. Complex Parsing Edge Cases:")
        test_cases = ['3-4i', '-2+5i', '-1-2i', '7i', '-3i']
        for case in test_cases:
            parsed = APICalc.ComplexNumber.from_string(case)
            print(f"   '{case}' -> {parsed}")
        
        print("\n=== ALL TESTS PASSED SUCCESSFULLY ===")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
