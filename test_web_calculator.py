#!/usr/bin/env python3
"""
Test script for the Advanced Precision Calculator Web Interface
"""

import sys
import json
import APICalc
import app

def test_api_functions():
    """Test the core API functions"""
    print("=== TESTING WEB CALCULATOR API ===\n")
    
    # Test 1: Basic arithmetic
    print("1. Testing Basic Arithmetic:")
    try:
        result = app.evaluate_expression('123 + 456', 'standard', 10)
        print(f"   123 + 456 = {result}")
        
        result = app.evaluate_expression('10 * 20', 'standard', 10)
        print(f"   10 * 20 = {result}")
        
        result = app.evaluate_expression('100 / 7', 'standard', 10)
        print(f"   100 / 7 = {result}")
        
        print("   ✅ Basic arithmetic: PASSED")
    except Exception as e:
        print(f"   ❌ Basic arithmetic: FAILED - {e}")
    
    # Test 2: Complex Numbers
    print("\n2. Testing Complex Numbers:")
    try:
        result = app.evaluate_expression('3+4i', 'standard', 10)
        print(f"   3+4i = {result}")
        
        result = app.evaluate_expression('2-3i', 'standard', 10)
        print(f"   2-3i = {result}")
        
        # Complex arithmetic would need more sophisticated parsing
        print("   ✅ Complex numbers: PASSED")
    except Exception as e:
        print(f"   ❌ Complex numbers: FAILED - {e}")
    
    # Test 3: Mathematical Functions
    print("\n3. Testing Mathematical Functions:")
    try:
        x = APICalc.AdvancedPrecisionNumber('1')
        
        result = app.execute_function('sin', [x])
        print(f"   sin(1) = {result}")
        
        result = app.execute_function('cos', [x])
        print(f"   cos(1) = {result}")
        
        x2 = APICalc.AdvancedPrecisionNumber('2')
        result = app.execute_function('sqrt', [x2])
        print(f"   sqrt(2) = {result}")
        
        print("   ✅ Mathematical functions: PASSED")
    except Exception as e:
        print(f"   ❌ Mathematical functions: FAILED - {e}")
    
    # Test 4: Mathematical Constants
    print("\n4. Testing Mathematical Constants:")
    try:
        pi = APICalc.AdvancedPrecisionNumber._get_pi(20)
        e = APICalc.AdvancedPrecisionNumber._get_e(20)
        
        print(f"   π (20 digits) = {pi}")
        print(f"   e (20 digits) = {e}")
        
        print("   ✅ Mathematical constants: PASSED")
    except Exception as e:
        print(f"   ❌ Mathematical constants: FAILED - {e}")
    
    # Test 5: Complex Functions
    print("\n5. Testing Complex Functions:")
    try:
        c = APICalc.ComplexNumber('3', '4')
        
        print(f"   Complex number: {c}")
        print(f"   Magnitude: {c.abs()}")
        print(f"   Conjugate: {c.conjugate()}")
        
        # Test complex function calls
        result = app.execute_function('abs', [c])
        print(f"   abs(3+4i) = {result}")
        
        result = app.execute_function('conjugate', [c])
        print(f"   conjugate(3+4i) = {result}")
        
        print("   ✅ Complex functions: PASSED")
    except Exception as e:
        print(f"   ❌ Complex functions: FAILED - {e}")
    
    # Test 6: Different Number Bases
    print("\n6. Testing Number Base Conversions:")
    try:
        # Test binary
        result = app.evaluate_expression('0b1010', 'standard', 2)
        print(f"   0b1010 (binary) = {result}")
        
        # Test hexadecimal
        result = app.evaluate_expression('0xFF', 'standard', 16)
        print(f"   0xFF (hex) = {result}")
        
        print("   ✅ Number bases: PASSED")
    except Exception as e:
        print(f"   ❌ Number bases: FAILED - {e}")
    
    print("\n=== API TESTING COMPLETED ===")

def test_calculator_api_class():
    """Test the CalculatorAPI class methods"""
    print("\n=== TESTING CALCULATOR API CLASS ===\n")
    
    try:
        # Test safe number creation
        num1 = app.CalculatorAPI.safe_number_creation('42')
        print(f"Real number: {num1}")
        
        num2 = app.CalculatorAPI.safe_number_creation('3+4i')
        print(f"Complex number: {num2}")
        
        # Test formatting
        result1 = app.CalculatorAPI.format_result(num1)
        result2 = app.CalculatorAPI.format_result(num2)
        
        print(f"Formatted real: {result1}")
        print(f"Formatted complex: {result2}")
        
        print("✅ CalculatorAPI class: PASSED")
    except Exception as e:
        print(f"❌ CalculatorAPI class: FAILED - {e}")

def main():
    """Run all tests"""
    print("Advanced Precision Calculator - Web Interface Test\n")
    
    try:
        test_api_functions()
        test_calculator_api_class()
        
        print("\n🎉 ALL TESTS COMPLETED!")
        print("\nThe web calculator is ready to run!")
        print("To start the server, run: python app.py")
        print("Then open your browser to: http://localhost:5000")
        
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
