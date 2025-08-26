#!/usr/bin/env python3
"""
Test script for matrix operations in APICalc
"""

def test_matrix_operations():
    print("Testing Matrix Operations in APICalc...")
    print("=" * 50)
    
    try:
        from matrix_operations import Matrix, matrix_add, matrix_subtract, matrix_multiply, matrix_transpose, matrix_determinant, matrix_inverse, matrix_trace
        from APICalc import AdvancedPrecisionNumber
        print("✓ Matrix operations imported successfully!")
    except ImportError as e:
        print(f"✗ Failed to import matrix operations: {e}")
        return False
    
    print("\n1. Creating matrices...")
    try:
        # Create test matrices
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])
        print(f"Matrix 1 (2x2):\n{m1}")
        print(f"Matrix 2 (2x2):\n{m2}")
        
        # Test identity matrix
        identity = Matrix.identity(3)
        print(f"3x3 Identity Matrix:\n{identity}")
        
        # Test zero matrix
        zeros = Matrix.zeros(2, 3)
        print(f"2x3 Zero Matrix:\n{zeros}")
        
        print("✓ Matrix creation successful!")
    except Exception as e:
        print(f"✗ Matrix creation failed: {e}")
        return False
    
    print("\n2. Testing matrix operations...")
    try:
        # Addition
        result_add = m1 + m2
        print(f"Addition Result:\n{result_add}")
        
        # Subtraction  
        result_sub = m1 - m2
        print(f"Subtraction Result:\n{result_sub}")
        
        # Multiplication
        result_mul = m1 * m2
        print(f"Multiplication Result:\n{result_mul}")
        
        # Transpose
        result_transpose = matrix_transpose(m1)
        print(f"Transpose of Matrix 1:\n{result_transpose}")
        
        # Determinant
        det = matrix_determinant(m1)
        print(f"Determinant of Matrix 1: {det}")
        
        # Trace
        tr = matrix_trace(m1)
        print(f"Trace of Matrix 1: {tr}")
        
        print("✓ Matrix operations successful!")
    except Exception as e:
        print(f"✗ Matrix operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n3. Testing complex matrices...")
    try:
        # Create complex matrix
        complex_matrix = Matrix([['1+2i', '3-i'], ['0+4i', '2']])
        print(f"Complex Matrix:\n{complex_matrix}")
        
        # Complex matrix operations
        complex_transpose = matrix_transpose(complex_matrix)
        print(f"Complex Matrix Transpose:\n{complex_transpose}")
        
        print("✓ Complex matrix operations successful!")
    except Exception as e:
        print(f"✗ Complex matrix operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n4. Testing parsing from strings...")
    try:
        # Test matrix parsing
        matrix_str = "[[1, 2, 3], [4, 5, 6]]"
        parsed_matrix = Matrix.from_string(matrix_str)
        print(f"Parsed Matrix from '{matrix_str}':\n{parsed_matrix}")
        
        print("✓ Matrix parsing successful!")
    except Exception as e:
        print(f"✗ Matrix parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("All matrix operations tests passed! ✓")
    return True

if __name__ == "__main__":
    test_matrix_operations()
