#!/usr/bin/env python3

from APICalc import AdvancedPrecisionNumber
import math

def test_trigonometric_functions():
    print("Testing trigonometric functions...")
    
    # Test sin
    print(f"sin(π/2) using π/2 ≈ 1.5708:")
    num1 = AdvancedPrecisionNumber('1.5708')
    result1 = num1.sin()
    print(f"  Result: {result1}")
    print(f"  Expected: ~1.0")
    
    # Test cos(0)
    print(f"\ncos(0):")
    num2 = AdvancedPrecisionNumber('0')
    result2 = num2.cos()
    print(f"  Result: {result2}")
    print(f"  Expected: 1.0")
    
    # Test tan(π/4)
    print(f"\ntan(π/4) using π/4 ≈ 0.7854:")
    num3 = AdvancedPrecisionNumber('0.7854')
    result3 = num3.tan()
    print(f"  Result: {result3}")
    print(f"  Expected: ~1.0")
    
    print("\nDirect API test complete.")

if __name__ == "__main__":
    test_trigonometric_functions()
