#!/usr/bin/env python3
"""
Test matrix operations through simulated REPL interaction
"""

def simulate_matrix_repl():
    print("Simulating Matrix REPL Operations...")
    print("=" * 50)
    
    try:
        from APICalc import calculate_repl
        from matrix_operations import Matrix
        
        # Test matrix function calls that the REPL should recognize
        test_commands = [
            "identity(3)",
            "zeros(2, 2)", 
            "ones(3, 2)",
            "transpose([[1, 2, 3], [4, 5, 6]])",
            "determinant([[1, 2], [3, 4]])",
            "trace([[1, 2, 3], [4, 5, 6], [7, 8, 9]])"
        ]
        
        print("Testing individual matrix functions:")
        
        # Test identity matrix function
        try:
            identity_3 = Matrix.identity(3)
            print(f"\nidentity(3):\n{identity_3}")
        except Exception as e:
            print(f"Error with identity(3): {e}")
        
        # Test zeros function
        try:
            zeros_2x2 = Matrix.zeros(2, 2)
            print(f"\nzeros(2, 2):\n{zeros_2x2}")
        except Exception as e:
            print(f"Error with zeros(2, 2): {e}")
            
        # Test ones function  
        try:
            ones_3x2 = Matrix.ones(3, 2)
            print(f"\nones(3, 2):\n{ones_3x2}")
        except Exception as e:
            print(f"Error with ones(3, 2): {e}")
        
        # Test matrix parsing and operations
        try:
            from matrix_operations import matrix_transpose, matrix_determinant, matrix_trace
            
            # Test transpose
            test_matrix = Matrix([[1, 2, 3], [4, 5, 6]])
            transposed = matrix_transpose(test_matrix)
            print(f"\ntranspose([[1, 2, 3], [4, 5, 6]]):\n{transposed}")
            
            # Test determinant
            square_matrix = Matrix([[1, 2], [3, 4]])
            det = matrix_determinant(square_matrix)
            print(f"\ndeterminant([[1, 2], [3, 4]]): {det}")
            
            # Test trace
            trace_matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            tr = matrix_trace(trace_matrix)
            print(f"\ntrace([[1, 2, 3], [4, 5, 6], [7, 8, 9]]): {tr}")
            
        except Exception as e:
            print(f"Error with matrix operations: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n" + "=" * 50)
        print("Matrix REPL simulation completed! ✓")
        
    except Exception as e:
        print(f"Error in matrix REPL simulation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_matrix_repl()
