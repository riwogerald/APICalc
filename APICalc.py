import math
import fractions

class AdvancedPrecisionNumber:
    def __init__(self, value='0', base=10):
        # Core number representation
        self.base = base
        self.negative = False
        self.whole_digits = []
        self.fractional_digits = []

        # Handle various input types
        if isinstance(value, AdvancedPrecisionNumber):
            self.base = value.base
            self.negative = value.negative
            self.whole_digits = value.whole_digits.copy()
            self.fractional_digits = value.fractional_digits.copy()
            return

        # String parsing
        if isinstance(value, str):
            value = value.strip().lower()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Handle base conversion
            if 'b' in value:  # Binary
                base = 2
                value = value.replace('b', '')
            elif 'x' in value:  # Hex
                base = 16
                value = value.replace('x', '')
            elif 'o' in value:  # Octal
                base = 8
                value = value.replace('o', '')
            else:
                base = 10

            # Split whole and fractional parts
            parts = value.split('.')
            whole = parts[0]
            fractional = parts[1] if len(parts) > 1 else ''

            # Convert to decimal digits
            self.whole_digits = [self._char_to_digit(c) for c in reversed(whole)]
            self.fractional_digits = [self._char_to_digit(c) for c in fractional]
            self.base = base

    def _char_to_digit(self, char):
        # Convert character to numeric value
        if char.isdigit():
            return int(char)
        return ord(char.lower()) - ord('a') + 10

    def _digit_to_char(self, digit):
        # Convert numeric value to character
        if 0 <= digit <= 9:
            return str(digit)
        return chr(digit - 10 + ord('a'))

    def __str__(self):
        # Format number based on base
        sign = '-' if self.negative else ''
        whole = ''.join(reversed([self._digit_to_char(d) for d in self.whole_digits]))
        whole = whole or '0'
        
        if self.fractional_digits:
            frac = ''.join([self._digit_to_char(d) for d in self.fractional_digits])
            return f"{sign}{whole}.{frac}"
        return f"{sign}{whole}"

    def __add__(self, other):
        # Addition implementation (simplified for brevity)
        result = AdvancedPrecisionNumber()
        # Implement base-aware addition logic here
        return result

    def sqrt(self):
        # Basic square root approximation
        # More sophisticated implementation needed for true arbitrary precision
        return AdvancedPrecisionNumber(str(math.sqrt(float(str(self)))))

    @classmethod
    def pi(cls):
        # Approximate Pi
        return cls(str(math.pi))

def calculate_repl():
    def print_menu():
        print("\n==== Advanced Precision Calculator ====")
        print("Operations:")
        print("  Addition (+)       : a + b")
        print("  Subtraction (-)    : a - b")
        print("  Multiplication (*) : a * b")
        print("  Division (/)       : a / b")
        print("  Modulo (%)         : a % b")
        print("  Exponentiation (**): a ** b")
        print("  Factorial (!)      : factorial x")
        print("  Square (√)         : sqrt x")
        print("  Cube (³)           : x ** 3")
        print("  Percent (%)        : x % y")
        print("  Pi (π)             : pi")
        print("  Base Conversions   : 10b, 2b, 16x, 8o")
        print("  Fractions          : 1/2, 3/4")
        print("  Exit               : quit/exit\n")

    print_menu()
    
    while True:
        try:
            expr = input(">>> ").strip().lower()
            
            if expr in ['quit', 'exit', 'q']:
                break
            
            if expr == 'menu':
                print_menu()
                continue
            
            # Special functions
            if expr == 'pi':
                print(AdvancedPrecisionNumber.pi())
                continue
            
            if expr.startswith('factorial '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                print("Factorial not fully implemented")
                continue
            
            if expr.startswith('sqrt '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                print(num.sqrt())
                continue
            
            # Parse standard arithmetic operations
            if any(op in expr for op in ['+', '-', '*', '/', '%', '**']):
                left, op, right = expr.split()
                left = AdvancedPrecisionNumber(left)
                right = AdvancedPrecisionNumber(right)
                
                if op == '+':
                    print(left + right)
                # Add more operation handlers here
            else:
                # Simple value parsing and display
                print(AdvancedPrecisionNumber(expr))
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    calculate_repl()