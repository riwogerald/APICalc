import math
import fractions

class AdvancedPrecisionNumber:
    def __init__(self, value='0', base=10, precision=50):
        # Enhanced initialization with explicit precision
        self.base = base
        self.precision = precision
        self.negative = False
        self.whole_digits = []
        self.fractional_digits = []

        # Handle various input types
        if isinstance(value, AdvancedPrecisionNumber):
            self.base = value.base
            self.precision = value.precision
            self.negative = value.negative
            self.whole_digits = value.whole_digits.copy()
            self.fractional_digits = value.fractional_digits.copy()
            return

        # Handle fractions
        if isinstance(value, fractions.Fraction):
            whole = value.numerator
            denom = value.denominator
            value = f"{whole}/{denom}"

        # String parsing with enhanced base handling
        if isinstance(value, str):
            value = value.strip().lower()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Fraction handling
            if '/' in value:
                num, denom = value.split('/')
                num_api = AdvancedPrecisionNumber(num, base, precision)
                denom_api = AdvancedPrecisionNumber(denom, base, precision)
                result = num_api / denom_api
                self.__dict__.update(result.__dict__)
                return

            # Improved base detection
            if value.startswith('0b'):  # Binary
                base = 2
                value = value[2:]
            elif value.startswith('0x'):  # Hex
                base = 16
                value = value[2:]
            elif value.startswith('0o'):  # Octal
                base = 8
                value = value[2:]
            else:
                base = base

            # Split whole and fractional parts
            parts = value.split('.')
            whole = parts[0]
            fractional = parts[1] if len(parts) > 1 else ''

            # Convert digits with base-aware conversion
            self.base = base
            self.whole_digits = self._convert_digits_to_decimal(whole)
            self.fractional_digits = self._convert_digits_to_decimal(fractional)
            
            # Trim or pad fractional digits to specified precision
            self.fractional_digits = self.fractional_digits[:precision]
            while len(self.fractional_digits) < precision:
                self.fractional_digits.append(0)

            # Ensure non-zero representation
            if not self.whole_digits:
                self.whole_digits = [0]

    def _convert_digits_to_decimal(self, digit_str):
        # Convert digits from current base to decimal representation
        return [self._char_to_digit(c) for c in reversed(digit_str) if c != '_']

    def _char_to_digit(self, char):
        # Convert character to numeric value with base support
        if char.isdigit():
            digit = int(char)
            if digit >= self.base:
                raise ValueError(f"Digit {digit} not valid in base {self.base}")
            return digit
        
        digit = ord(char.lower()) - ord('a') + 10
        if digit >= self.base:
            raise ValueError(f"Digit {char} not valid in base {self.base}")
        return digit

    def _digit_to_char(self, digit):
        # Convert numeric value to character with base support
        if 0 <= digit < 10:
            return str(digit)
        if 10 <= digit < 36:
            return chr(digit - 10 + ord('a'))
        raise ValueError(f"Cannot represent digit {digit} in base {self.base}")

    def _base_convert(self, target_base):
        # Convert whole part
        whole_decimal = sum(digit * (self.base ** power) 
                        for power, digit in enumerate(self.whole_digits))
    
        # Convert whole part to target base
        new_whole_digits = []
        while whole_decimal > 0:
            new_whole_digits.insert(0, whole_decimal % target_base)
            whole_decimal //= target_base
    
        # Convert fractional part
        frac_decimal = sum(digit * (self.base ** -(power+1)) 
                       for power, digit in enumerate(self.fractional_digits))
    
        # Convert fractional part to target base
        new_frac_digits = []
        for _ in range(self.precision):
            frac_decimal *= target_base
            digit = int(frac_decimal)
            new_frac_digits.append(digit)
            frac_decimal -= digit
    
        # Create new AdvancedPrecisionNumber
        new_num = AdvancedPrecisionNumber('0', target_base, self.precision)
        new_num.whole_digits = new_whole_digits if new_whole_digits else [0]
        new_num.fractional_digits = new_frac_digits
        new_num.negative = self.negative
    
        return new_num

    def _to_decimal(self):
        # Convert current representation to decimal float
        whole = sum(digit * (self.base ** power) for power, digit in enumerate(self.whole_digits))
        frac = sum(digit * (self.base ** -(power+1)) for power, digit in enumerate(self.fractional_digits))
        return whole + frac

    def _from_decimal(self, decimal_value, base):
        # Create new AdvancedPrecisionNumber from decimal value in specified base
        new_num = AdvancedPrecisionNumber('0', base, self.precision)
        new_num.negative = decimal_value < 0
        decimal_value = abs(decimal_value)

        # Whole part conversion
        whole_part = int(decimal_value)
        new_num.whole_digits = []
        while whole_part > 0:
            new_num.whole_digits.insert(0, whole_part % base)
            whole_part //= base

        # Fractional part conversion
        frac_part = decimal_value - int(decimal_value)
        new_num.fractional_digits = []
        for _ in range(self.precision):
            frac_part *= base
            digit = int(frac_part)
            new_num.fractional_digits.append(digit)
            frac_part -= digit

        return new_num

    def __str__(self):
        # Enhanced string representation with base prefix
        sign = '-' if self.negative else ''
        whole = ''.join(reversed([self._digit_to_char(d) for d in self.whole_digits]))
        whole = whole or '0'
        
        base_prefix = {2: '0b', 8: '0o', 10: '', 16: '0x'}.get(self.base, f'[base{self.base}]')
        
        if self.fractional_digits:
            frac = ''.join([self._digit_to_char(d) for d in self.fractional_digits])
            return f"{sign}{base_prefix}{whole}.{frac}"
        return f"{sign}{base_prefix}{whole}"

    # Existing comparison and arithmetic methods remain largely the same
    def __lt__(self, other):
        other = self._ensure_apn(other)
        # Convert to decimal for comparison
        return self._to_decimal() < other._to_decimal()

    def __eq__(self, other):
        other = self._ensure_apn(other)
        # Convert to decimal for comparison
        return abs(self._to_decimal() - other._to_decimal()) < 1e-10

    def _ensure_apn(self, other):
        return other if isinstance(other, AdvancedPrecisionNumber) else AdvancedPrecisionNumber(other, self.base, self.precision)

    def __add__(self, other):
        other = self._ensure_apn(other)
        decimal_sum = self._to_decimal() + other._to_decimal()
        return self._from_decimal(decimal_sum, self.base)

    def __sub__(self, other):
        other = self._ensure_apn(other)
        decimal_diff = self._to_decimal() - other._to_decimal()
        return self._from_decimal(decimal_diff, self.base)

    def __mul__(self, other):
        other = self._ensure_apn(other)
        decimal_product = self._to_decimal() * other._to_decimal()
        result = self._from_decimal(decimal_product, self.base)
        result.negative = self.negative != other.negative
        return result

    def __truediv__(self, other):
        other = self._ensure_apn(other)
        if abs(other._to_decimal()) < 1e-10:
            raise ZeroDivisionError("Division by zero")
        
        decimal_quotient = self._to_decimal() / other._to_decimal()
        result = self._from_decimal(decimal_quotient, self.base)
        result.negative = self.negative != other.negative
        return result

    def __mod__(self, other):
        other = self._ensure_apn(other)
        if abs(other._to_decimal()) < 1e-10:
            raise ZeroDivisionError("Modulo by zero")
        
        decimal_mod = self._to_decimal() % other._to_decimal()
        return self._from_decimal(decimal_mod, self.base)

    def __pow__(self, other):
        other = self._ensure_apn(other)
        decimal_power = self._to_decimal() ** other._to_decimal()
        result = self._from_decimal(decimal_power, self.base)
        
        # Handle sign for integer exponents
        if other.fractional_digits == [0] * len(other.fractional_digits):
            result.negative = self.negative and (int(other._to_decimal()) % 2 == 1)
        
        return result
    
    def sqrt(self):
        return self._from_decimal(math.sqrt(self._to_decimal()), self.base)

    def sqr(self):
        return self * self

    def cube(self):
        return self ** AdvancedPrecisionNumber('3', self.base, self.precision)

    def cube_root(self):
        return self._from_decimal(self._to_decimal() ** (1/3), self.base)

    def reciprocal(self):
        return AdvancedPrecisionNumber('1', self.base, self.precision) / self

    def factorial(self):
        if self.negative or self.fractional_digits != [0] * len(self.fractional_digits):
            raise ValueError("Factorial is only defined for non-negative integers")
        n = int(self._to_decimal())
        result = math.factorial(n)  # Use built-in math.factorial for efficiency    
        return self._from_decimal(result, self.base)
        
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

    def perform_unary_operation(operation, expr):
        num = AdvancedPrecisionNumber(expr.split()[1])
        result = getattr(num, operation)()
        print(result)
        calculation_history.append(f"{operation} {num} = {result}")
   
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

            # Unified unary operation handling
            unary_ops = {
                'factorial': 'factorial',
                'sqrt': 'sqrt',
                'sqr': 'sqr',
                'cube': 'cube',
                'cube_root': 'cube_root',
                'reciprocal': 'reciprocal'
            }
            
            for prefix, method in unary_ops.items():
                if expr.startswith(f'{prefix} ') or (method == 'factorial' and expr.endswith('!')):
                    num_expr = expr.split()[1] if not expr.endswith('!') else expr[:-1]
                    perform_unary_operation(method, f'{prefix} {num_expr}')
                    break
            else:
            
            # Special functions
                if expr.startswith('factorial '):
                    num = AdvancedPrecisionNumber(expr.split()[1])
                    result = num.factorial()
                    print(result)
                    calculation_history.append(f"factorial {num} = {result}")
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

             # Factorial implementation
            if expr.startswith('factorial ') or expr.endswith('!'):
                if expr.startswith('factorial '):
                    num = AdvancedPrecisionNumber(expr.split()[1])
                else:
                    num = AdvancedPrecisionNumber(expr[:-1])
                
                result = num.factorial()
                print(result)
                calculation_history.append(f"factorial {num} = {result}")
                continue
            
             # Percent and modulo handling
            if '%' in expr:
                left, right = expr.split('%')
                left = AdvancedPrecisionNumber(left.strip())
                
                if 'of' in right:
                    # Percent calculation: a % of b
                    right = AdvancedPrecisionNumber(right.split('of')[1].strip())
                    result = (left / AdvancedPrecisionNumber('100')) * right
                    print(result)
                    calculation_history.append(f"{left}% of {right} = {result}")
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