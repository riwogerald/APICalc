import math
import fractions

class AdvancedPrecisionNumber:
    def __init__(self, value='0', base=10):
        # Core number representation
        self.base = base
        self.negative = False
        self.whole_digits = []
        self.fractional_digits = []
        self.calculation_history = []

        # Handle various input types
        if isinstance(value, AdvancedPrecisionNumber):
            self.base = value.base
            self.negative = value.negative
            self.whole_digits = value.whole_digits.copy()
            self.fractional_digits = value.fractional_digits.copy()
            return

        # Handle fractions
        if isinstance(value, fractions.Fraction):
            whole = value.numerator
            denom = value.denominator
            value = f"{whole}/{denom}"

        # String parsing
        if isinstance(value, str):
            value = value.strip().lower()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Handle fraction representation
            if '/' in value:
                num, denom = value.split('/')
                num_api = AdvancedPrecisionNumber(num)
                denom_api = AdvancedPrecisionNumber(denom)
                result = num_api / denom_api
                self.whole_digits = result.whole_digits
                self.fractional_digits = result.fractional_digits
                self.negative = result.negative
                return

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
            
            # Ensure non-zero representation
            if not self.whole_digits:
                self.whole_digits = [0]

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

    def __repr__(self):
        return f"AdvancedPrecisionNumber('{self}')"

    def __abs__(self):
        result = AdvancedPrecisionNumber(self)
        result.negative = False
        return result

    def __lt__(self, other):
        other = self._ensure_apn(other)
        if self.negative != other.negative:
            return self.negative
        
        # Compare whole part
        if len(self.whole_digits) != len(other.whole_digits):
            return (len(self.whole_digits) < len(other.whole_digits)) ^ self.negative
        
        # Compare digit by digit
        for a, b in zip(reversed(self.whole_digits), reversed(other.whole_digits)):
            if a != b:
                return (a < b) ^ self.negative
        
        # Compare fractional part if whole parts are equal
        frac_len = max(len(self.fractional_digits), len(other.fractional_digits))
        for i in range(frac_len):
            a = self.fractional_digits[i] if i < len(self.fractional_digits) else 0
            b = other.fractional_digits[i] if i < len(other.fractional_digits) else 0
            if a != b:
                return (a < b) ^ self.negative
        
        return False

    def __eq__(self, other):
        other = self._ensure_apn(other)
        return (self.whole_digits == other.whole_digits and 
                self.fractional_digits == other.fractional_digits and 
                self.negative == other.negative)

    def _ensure_apn(self, other):
        return other if isinstance(other, AdvancedPrecisionNumber) else AdvancedPrecisionNumber(other)

    def __add__(self, other):
        other = self._ensure_apn(other)
        
        # If signs differ, use subtraction
        if self.negative != other.negative:
            if self.negative:
                return other - abs(self)
            return self - abs(other)
        
        # Implement addition
        result = AdvancedPrecisionNumber(str(float(str(self)) + float(str(other))))
        result.negative = self.negative
        return result

    def __sub__(self, other):
        other = self._ensure_apn(other)
        return AdvancedPrecisionNumber(str(float(str(self)) - float(str(other))))

    def __mul__(self, other):
        other = self._ensure_apn(other)
        
        # Determine sign
        result = AdvancedPrecisionNumber(str(float(str(self)) * float(str(other))))
        result.negative = self.negative != other.negative
        return result

    def __truediv__(self, other):
        other = self._ensure_apn(other)
        
        if str(other) == '0':
            raise ZeroDivisionError("Division by zero")
        
        return AdvancedPrecisionNumber(str(float(str(self)) / float(str(other))))

    def __mod__(self, other):
        other = self._ensure_apn(other)
        
        if str(other) == '0':
            raise ZeroDivisionError("Modulo by zero")
        
        return AdvancedPrecisionNumber(str(int(float(str(self))) % int(float(str(other)))))

    def __pow__(self, other):
        other = self._ensure_apn(other)
        
        # Determine sign (only for integer exponents)
        result = AdvancedPrecisionNumber(str(float(str(self)) ** float(str(other))))
        result.negative = self.negative and (float(str(other)) % 2 == 1)
        return result

    def sqrt(self):
        # Basic square root
        return AdvancedPrecisionNumber(str(math.sqrt(float(str(self)))))

    def sqr(self):
        # Square of the number
        return self * self

    def cube(self):
        # Cube of the number
        return self ** AdvancedPrecisionNumber('3')

    def cube_root(self):
        # Basic cube root
        return AdvancedPrecisionNumber(str(float(str(self)) ** (1/3)))

    def reciprocal(self):
        # Return 1 divided by the number
        return AdvancedPrecisionNumber('1') / self

def calculate_repl():
    calculation_history = []

    def print_menu():
        print("\n==== Advanced Precision Calculator ====")
        print("Operations:")
        print("  Addition (+)       : a + b")
        print("  Subtraction (-)    : a - b")
        print("  Multiplication (*) : a * b")
        print("  Division (/)       : a / b")
        print("  Modulo (mod)       : a mod b")
        print("  Percent (%)        : a % of b")
        print("  Exponentiation (**): a ** b")
        print("  Factorial (!)      : factorial x")
        print("  Square Root (√)    : sqrt x")
        print("  Square (sqr)       : sqr x")
        print("  Cube (³)           : cube x")
        print("  Cube Root (∛)      : cube_root x")
        print("  Reciprocal (1/x)   : reciprocal x")
        print("  Base Conversions   : 10b, 2b, 16x, 8o")
        print("  Fractions          : 1/2, 3/4")
        print("  Clear History      : clear")
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
            
            if expr == 'clear':
                calculation_history.clear()
                print("Calculation history cleared.")
                continue
            
            # Special functions
            if expr.startswith('factorial '):
                print("Factorial not fully implemented")
                continue
            
            if expr.startswith('sqrt '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                result = num.sqrt()
                print(result)
                calculation_history.append(f"sqrt {num} = {result}")
                continue
            
            if expr.startswith('sqr '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                result = num.sqr()
                print(result)
                calculation_history.append(f"sqr {num} = {result}")
                continue
            
            if expr.startswith('cube '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                result = num.cube()
                print(result)
                calculation_history.append(f"cube {num} = {result}")
                continue
            
            if expr.startswith('cube_root '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                result = num.cube_root()
                print(result)
                calculation_history.append(f"cube_root {num} = {result}")
                continue
            
            if expr.startswith('reciprocal '):
                num = AdvancedPrecisionNumber(expr.split()[1])
                result = num.reciprocal()
                print(result)
                calculation_history.append(f"reciprocal {num} = {result}")
                continue
            
            # Disambiguated percent and modulo
            if '%' in expr:
                left, right = expr.split('%')
                left = AdvancedPrecisionNumber(left.strip())
                
                if 'of' in right:
                    # Percent calculation
                    right = AdvancedPrecisionNumber(right.split('of')[0].strip())
                    result = (left * right) / AdvancedPrecisionNumber('100')
                    print(result)
                    calculation_history.append(f"{left} % of {right} = {result}")
                else:
                    # Modulo operation
                    right = AdvancedPrecisionNumber(right.strip())
                    result = left % right
                    print(result)
                    calculation_history.append(f"{left} mod {right} = {result}")
                continue
            
            # Standard arithmetic operations
            if any(op in expr for op in ['+', '-', '*', '/', '**', 'mod']):
                parts = expr.split()
                
                if len(parts) == 3:
                    left, op, right = parts
                    left = AdvancedPrecisionNumber(left)
                    right = AdvancedPrecisionNumber(right)
                    
                    if op == '+':
                        result = left + right
                    elif op == '-':
                        result = left - right
                    elif op == '*':
                        result = left * right
                    elif op == '/':
                        result = left / right
                    elif op == '**':
                        result = left ** right
                    elif op == 'mod':
                        result = left % right
                    
                    print(result)
                    calculation_history.append(f"{left} {op} {right} = {result}")
                continue
            else:
                # Simple value parsing and display
                result = AdvancedPrecisionNumber(expr)
                print(result)
                calculation_history.append(f"{expr}")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    calculate_repl()