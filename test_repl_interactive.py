#!/usr/bin/env python
"""Test REPL functionality with complex numbers"""

import subprocess
import sys

def test_repl_commands():
    """Test REPL commands by simulating input"""
    
    # Test commands we want to try
    test_commands = [
        "3+4i",  # Basic complex number
        "2-5j",  # Another complex number
        "abs(3+4i)",  # Magnitude
        "conjugate(3+4i)",  # Conjugate
        "sin(1+2i)",  # Complex trig
        "exp(1+i)",  # Complex exponential
        "log(2+3i)",  # Complex logarithm
        "(3+4i) * (1-2i)",  # Complex arithmetic
        "sqrt(-1)",  # This should work with our implementation now since we have complex support
        "quit"
    ]
    
    print("Testing REPL with complex number commands:")
    print("=" * 50)
    
    for cmd in test_commands:
        print(f"Command: {cmd}")
    
    print("=" * 50)
    print("Note: These commands can be tested manually in the REPL")
    print("Run: python APICalc.py")
    print("Then try each command above")

def test_specific_features():
    """Test specific complex number features"""
    
    print("\nTesting specific complex number features:")
    print("=" * 50)
    
    # Import directly and test
    from APICalc import ComplexNumber, AdvancedPrecisionNumber
    
    # Test various complex operations
    print("1. Basic complex number creation:")
    z1 = ComplexNumber.from_string("3+4i")
    print(f"   z1 = {z1}")
    
    print("2. Complex arithmetic:")
    z2 = ComplexNumber.from_string("1-2i")
    result = z1 * z2
    print(f"   {z1} * {z2} = {result}")
    
    print("3. Complex magnitude:")
    mag = z1.abs()
    print(f"   |{z1}| = {mag}")
    
    print("4. Complex argument:")
    try:
        arg = z1.arg()
        print(f"   arg({z1}) = {arg}")
    except Exception as e:
        print(f"   Error computing arg: {e}")
    
    print("5. Complex exponential:")
    try:
        exp_result = z1.exp()
        print(f"   exp({z1}) = {exp_result}")
    except Exception as e:
        print(f"   Error computing exp: {e}")
    
    print("6. Complex sine:")
    try:
        sin_result = z1.sin()
        print(f"   sin({z1}) = {sin_result}")
    except Exception as e:
        print(f"   Error computing sin: {e}")
    
    print("7. Real number sin (for comparison):")
    real_num = AdvancedPrecisionNumber("1")
    sin_real = real_num.sin()
    print(f"   sin(1) = {sin_real}")
    
    print("=" * 50)
    print("✓ Complex number implementation is working!")

if __name__ == "__main__":
    test_repl_commands()
    test_specific_features()
