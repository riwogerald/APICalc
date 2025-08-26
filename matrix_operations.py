# Pure implementation of Matrix Operations - no external library dependencies
# Uses AdvancedPrecisionNumber and ComplexNumber for arbitrary precision matrix operations

from APICalc import AdvancedPrecisionNumber, ComplexNumber
import sys

class Matrix:
    """
    Pure implementation of Matrix operations using arbitrary precision numbers.
    Supports real and complex matrices with full arbitrary precision arithmetic.
    """
    
    def __init__(self, data=None, rows=0, cols=0, precision_mode='standard'):
        """
        Initialize a matrix.
        
        Args:
            data: List of lists, list of values, or None
            rows: Number of rows (if creating empty matrix)
            cols: Number of columns (if creating empty matrix)
            precision_mode: Precision mode for calculations
        """
        self.precision_mode = precision_mode
        self.precision = AdvancedPrecisionNumber.PRECISION_MODES.get(precision_mode, precision_mode)
        
        if data is not None:
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], list):
                    # 2D list provided
                    self.rows = len(data)
                    self.cols = len(data[0]) if self.rows > 0 else 0
                    self.data = []
                    
                    for i in range(self.rows):
                        row = []
                        for j in range(self.cols):
                            if j < len(data[i]):
                                element = data[i][j]
                                row.append(self._create_number(element))
                            else:
                                row.append(self._create_number('0'))
                        self.data.append(row)
                else:
                    # 1D list provided - treat as single row
                    self.rows = 1
                    self.cols = len(data)
                    self.data = [[self._create_number(element) for element in data]]
            else:
                # Empty data, use dimensions
                self.rows = max(rows, 0)
                self.cols = max(cols, 0)
                self.data = [[self._create_number('0') for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            # Create empty matrix with specified dimensions
            self.rows = max(rows, 0)
            self.cols = max(cols, 0)
            self.data = [[self._create_number('0') for _ in range(self.cols)] for _ in range(self.rows)]
    
    def _create_number(self, value):
        """Create appropriate number type (real or complex) from value."""
        if isinstance(value, (AdvancedPrecisionNumber, ComplexNumber)):
            return value
        
        value_str = str(value).strip()
        
        # Check if it's a complex number
        if 'i' in value_str or 'j' in value_str:
            return ComplexNumber.from_string(value_str)
        else:
            return AdvancedPrecisionNumber(value_str, precision_mode=self.precision_mode)
    
    def __str__(self):
        """String representation of matrix."""
        if self.rows == 0 or self.cols == 0:
            return "[]"
        
        # Calculate column widths for nice formatting
        col_widths = [0] * self.cols
        str_data = []
        
        for i in range(self.rows):
            row_strs = []
            for j in range(self.cols):
                elem_str = str(self.data[i][j])
                row_strs.append(elem_str)
                col_widths[j] = max(col_widths[j], len(elem_str))
            str_data.append(row_strs)
        
        # Build formatted string
        result = "[\n"
        for i in range(self.rows):
            result += "  ["
            for j in range(self.cols):
                result += f"{str_data[i][j]:>{col_widths[j]}}"
                if j < self.cols - 1:
                    result += ", "
            result += "]"
            if i < self.rows - 1:
                result += ","
            result += "\n"
        result += "]"
        
        return result
    
    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols})"
    
    def shape(self):
        """Return matrix dimensions as tuple."""
        return (self.rows, self.cols)
    
    def get(self, row, col):
        """Get element at specified position (0-indexed)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        else:
            raise IndexError(f"Matrix index out of bounds: ({row}, {col})")
    
    def set(self, row, col, value):
        """Set element at specified position (0-indexed)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = self._create_number(value)
        else:
            raise IndexError(f"Matrix index out of bounds: ({row}, {col})")
    
    def is_square(self):
        """Check if matrix is square."""
        return self.rows == self.cols and self.rows > 0
    
    def is_empty(self):
        """Check if matrix is empty."""
        return self.rows == 0 or self.cols == 0
    
    def copy(self):
        """Create a deep copy of the matrix."""
        new_matrix = Matrix(rows=self.rows, cols=self.cols, precision_mode=self.precision_mode)
        for i in range(self.rows):
            for j in range(self.cols):
                new_matrix.data[i][j] = self.data[i][j]
        return new_matrix
    
    # Matrix Arithmetic Operations
    
    def __add__(self, other):
        """Matrix addition."""
        if not isinstance(other, Matrix):
            raise TypeError("Can only add matrices to matrices")
        
        if self.shape() != other.shape():
            raise ValueError(f"Cannot add matrices with shapes {self.shape()} and {other.shape()}")
        
        result = Matrix(rows=self.rows, cols=self.cols, precision_mode=self.precision_mode)
        
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        
        return result
    
    def __sub__(self, other):
        """Matrix subtraction."""
        if not isinstance(other, Matrix):
            raise TypeError("Can only subtract matrices from matrices")
        
        if self.shape() != other.shape():
            raise ValueError(f"Cannot subtract matrices with shapes {self.shape()} and {other.shape()}")
        
        result = Matrix(rows=self.rows, cols=self.cols, precision_mode=self.precision_mode)
        
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        
        return result
    
    def __mul__(self, other):
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, Matrix):
            # Matrix multiplication
            if self.cols != other.rows:
                raise ValueError(f"Cannot multiply {self.shape()} matrix with {other.shape()} matrix")
            
            result = Matrix(rows=self.rows, cols=other.cols, precision_mode=self.precision_mode)
            
            for i in range(self.rows):
                for j in range(other.cols):
                    sum_val = self._create_number('0')
                    for k in range(self.cols):
                        product = self.data[i][k] * other.data[k][j]
                        sum_val = sum_val + product
                    result.data[i][j] = sum_val
            
            return result
        else:
            # Scalar multiplication
            scalar = self._create_number(other)
            result = Matrix(rows=self.rows, cols=self.cols, precision_mode=self.precision_mode)
            
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] * scalar
            
            return result
    
    def __rmul__(self, other):
        """Right scalar multiplication."""
        return self.__mul__(other)
    
    def scalar_multiply(self, scalar):
        """Scalar multiplication (explicit method)."""
        return self * scalar
    
    def transpose(self):
        """Return transpose of the matrix."""
        result = Matrix(rows=self.cols, cols=self.rows, precision_mode=self.precision_mode)
        
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[j][i] = self.data[i][j]
        
        return result
    
    def trace(self):
        """Calculate trace (sum of diagonal elements) for square matrices."""
        if not self.is_square():
            raise ValueError("Trace is only defined for square matrices")
        
        trace_sum = self._create_number('0')
        for i in range(self.rows):
            trace_sum = trace_sum + self.data[i][i]
        
        return trace_sum
    
    def determinant(self):
        """Calculate determinant using recursive cofactor expansion."""
        if not self.is_square():
            raise ValueError("Determinant is only defined for square matrices")
        
        if self.rows == 0:
            return self._create_number('1')
        elif self.rows == 1:
            return self.data[0][0]
        elif self.rows == 2:
            # 2x2 determinant: ad - bc
            a = self.data[0][0]
            b = self.data[0][1]
            c = self.data[1][0]
            d = self.data[1][1]
            return (a * d) - (b * c)
        else:
            # Recursive cofactor expansion along first row
            det = self._create_number('0')
            
            for j in range(self.cols):
                # Get cofactor
                minor = self._get_minor(0, j)
                cofactor = minor.determinant()
                
                # Apply sign
                if j % 2 == 1:
                    cofactor = self._create_number('0') - cofactor
                
                # Add to determinant
                term = self.data[0][j] * cofactor
                det = det + term
            
            return det
    
    def _get_minor(self, exclude_row, exclude_col):
        """Get minor matrix by excluding specified row and column."""
        if self.rows <= 1 or self.cols <= 1:
            return Matrix(precision_mode=self.precision_mode)
        
        minor_data = []
        for i in range(self.rows):
            if i == exclude_row:
                continue
            row = []
            for j in range(self.cols):
                if j == exclude_col:
                    continue
                row.append(self.data[i][j])
            minor_data.append(row)
        
        return Matrix(minor_data, precision_mode=self.precision_mode)
    
    def inverse(self):
        """Calculate matrix inverse using Gauss-Jordan elimination."""
        if not self.is_square():
            raise ValueError("Inverse is only defined for square matrices")
        
        det = self.determinant()
        zero = self._create_number('0')
        
        # Check if determinant is zero (using comparison with small epsilon)
        try:
            if isinstance(det, AdvancedPrecisionNumber):
                det_val = det._base_to_decimal()
            elif isinstance(det, ComplexNumber):
                det_val = det.abs()._base_to_decimal()
            else:
                det_val = float(str(det))
            
            if abs(det_val) < 10**(-self.precision + 5):
                raise ValueError("Matrix is singular (determinant is zero)")
        except:
            raise ValueError("Could not determine if matrix is singular")
        
        n = self.rows
        
        # Create augmented matrix [A|I]
        augmented = Matrix(rows=n, cols=2*n, precision_mode=self.precision_mode)
        
        # Fill in A
        for i in range(n):
            for j in range(n):
                augmented.data[i][j] = self.data[i][j]
        
        # Fill in I (identity matrix)
        for i in range(n):
            for j in range(n):
                if i == j:
                    augmented.data[i][n + j] = self._create_number('1')
                else:
                    augmented.data[i][n + j] = self._create_number('0')
        
        # Perform Gauss-Jordan elimination
        for i in range(n):
            # Find pivot
            pivot_row = i
            for k in range(i + 1, n):
                if self._abs_value(augmented.data[k][i]) > self._abs_value(augmented.data[pivot_row][i]):
                    pivot_row = k
            
            # Swap rows if needed
            if pivot_row != i:
                augmented.data[i], augmented.data[pivot_row] = augmented.data[pivot_row], augmented.data[i]
            
            # Make diagonal element 1
            pivot = augmented.data[i][i]
            if self._abs_value(pivot) < 10**(-self.precision + 5):
                raise ValueError("Matrix is singular")
            
            for j in range(2 * n):
                augmented.data[i][j] = augmented.data[i][j] / pivot
            
            # Make other elements in column 0
            for k in range(n):
                if k != i:
                    factor = augmented.data[k][i]
                    for j in range(2 * n):
                        product = factor * augmented.data[i][j]
                        augmented.data[k][j] = augmented.data[k][j] - product
        
        # Extract inverse matrix (right half of augmented matrix)
        inverse_matrix = Matrix(rows=n, cols=n, precision_mode=self.precision_mode)
        for i in range(n):
            for j in range(n):
                inverse_matrix.data[i][j] = augmented.data[i][j + n]
        
        return inverse_matrix
    
    def _abs_value(self, number):
        """Get absolute value of a number (real or complex)."""
        if isinstance(number, ComplexNumber):
            return number.abs()._base_to_decimal()
        elif isinstance(number, AdvancedPrecisionNumber):
            return abs(number._base_to_decimal())
        else:
            return abs(float(str(number)))
    
    # Static factory methods
    
    @staticmethod
    def identity(size, precision_mode='standard'):
        """Create identity matrix of given size."""
        matrix = Matrix(rows=size, cols=size, precision_mode=precision_mode)
        
        for i in range(size):
            for j in range(size):
                if i == j:
                    matrix.data[i][j] = matrix._create_number('1')
                else:
                    matrix.data[i][j] = matrix._create_number('0')
        
        return matrix
    
    @staticmethod
    def zeros(rows, cols, precision_mode='standard'):
        """Create matrix filled with zeros."""
        return Matrix(rows=rows, cols=cols, precision_mode=precision_mode)
    
    @staticmethod
    def ones(rows, cols, precision_mode='standard'):
        """Create matrix filled with ones."""
        matrix = Matrix(rows=rows, cols=cols, precision_mode=precision_mode)
        
        for i in range(rows):
            for j in range(cols):
                matrix.data[i][j] = matrix._create_number('1')
        
        return matrix
    
    @staticmethod
    def from_string(matrix_str, precision_mode='standard'):
        """Parse matrix from string representation."""
        matrix_str = matrix_str.strip()
        
        # Remove outer brackets
        if matrix_str.startswith('[') and matrix_str.endswith(']'):
            matrix_str = matrix_str[1:-1].strip()
        
        # Split into rows
        rows = []
        current_row = ""
        bracket_count = 0
        
        for char in matrix_str:
            if char == '[':
                bracket_count += 1
                if bracket_count == 1:
                    current_row = ""
                else:
                    current_row += char
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    if current_row.strip():
                        rows.append(current_row.strip())
                    current_row = ""
                else:
                    current_row += char
            elif bracket_count > 0:
                current_row += char
        
        # Parse each row
        data = []
        for row_str in rows:
            elements = []
            for elem_str in row_str.split(','):
                elem_str = elem_str.strip()
                if elem_str:
                    elements.append(elem_str)
            if elements:
                data.append(elements)
        
        if not data:
            return Matrix(precision_mode=precision_mode)
        
        return Matrix(data, precision_mode=precision_mode)

# Helper functions for integration with REPL

def matrix_add(matrix1, matrix2):
    """Add two matrices."""
    return matrix1 + matrix2

def matrix_subtract(matrix1, matrix2):
    """Subtract matrix2 from matrix1."""
    return matrix1 - matrix2

def matrix_multiply(matrix1, matrix2):
    """Multiply two matrices or matrix by scalar."""
    return matrix1 * matrix2

def matrix_transpose(matrix):
    """Return transpose of matrix."""
    return matrix.transpose()

def matrix_determinant(matrix):
    """Calculate determinant of matrix."""
    return matrix.determinant()

def matrix_inverse(matrix):
    """Calculate inverse of matrix."""
    return matrix.inverse()

def matrix_trace(matrix):
    """Calculate trace of matrix."""
    return matrix.trace()

# Example usage and testing
if __name__ == "__main__":
    print("Matrix Operations - Pure Implementation Test")
    print("=" * 50)
    
    try:
        # Test basic matrix creation
        print("\n1. Matrix Creation:")
        m1 = Matrix([[1, 2], [3, 4]])
        print(f"Matrix m1:\n{m1}")
        
        m2 = Matrix([[5, 6], [7, 8]])
        print(f"Matrix m2:\n{m2}")
        
        # Test addition
        print("\n2. Matrix Addition:")
        m3 = m1 + m2
        print(f"m1 + m2:\n{m3}")
        
        # Test multiplication
        print("\n3. Matrix Multiplication:")
        m4 = m1 * m2
        print(f"m1 * m2:\n{m4}")
        
        # Test transpose
        print("\n4. Matrix Transpose:")
        m5 = m1.transpose()
        print(f"m1^T:\n{m5}")
        
        # Test determinant
        print("\n5. Matrix Determinant:")
        det = m1.determinant()
        print(f"det(m1) = {det}")
        
        # Test identity matrix
        print("\n6. Identity Matrix:")
        identity = Matrix.identity(3)
        print(f"I(3):\n{identity}")
        
        # Test complex matrix
        print("\n7. Complex Matrix:")
        complex_m = Matrix([['1+2i', '3'], ['4i', '5-1i']])
        print(f"Complex matrix:\n{complex_m}")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
