import math
import fractions
import sys

class AdvancedPrecisionNumber:
    def __init__(self, value='0', base=10, precision=50):
        self.base = base
        self.precision = precision
        self.negative = False
        self.whole_digits = [0]
        self.fractional_digits = [0] * precision

        # Fraction support
        self.fraction = None
        
        # Handle fraction input
        if fraction is not None:
            # If fraction is provided, convert it
            if isinstance(fraction, (int, float, str)):
                fraction = fractions.Fraction(fraction)
            
            if isinstance(fraction, fractions.Fraction):
                # Store the fraction
                self.fraction = fraction
                
                # Convert fraction to decimal for base conversion
                decimal_value = float(fraction)
                value = str(decimal_value)
        
        # Handle various input types and parsing
        if isinstance(value, AdvancedPrecisionNumber):
            self.base = value.base
            self.precision = value.precision
            self.negative = value.negative
            self.whole_digits = value.whole_digits.copy()
            self.fractional_digits = value.fractional_digits.copy()
            return

        # String parsing with enhanced base and fraction handling
        if isinstance(value, str):
            value = value.strip().lower()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Base detection
            if value.startswith('0b'):  # Binary
                base = 2
                value = value[2:]
            elif value.startswith('0x'):  # Hex
                base = 16
                value = value[2:]
            elif value.startswith('0o'):  # Octal
                base = 8
                value = value[2:]
            
            self.base = base

            # Split whole and fractional parts
            parts = value.split('.')
            whole = parts[0] or '0'
            fractional = parts[1] if len(parts) > 1 else ''

            # Convert digits
            self.whole_digits = [self._char_to_digit(c) for c in whole.replace('_', '')]
            self.fractional_digits = [self._char_to_digit(c) for c in fractional.replace('_', '')]
            
            # Trim or pad fractional digits
            self.fractional_digits = self.fractional_digits[:precision]
            while len(self.fractional_digits) < precision:
                self.fractional_digits.append(0)

    def _char_to_digit(self, char):
        # Convert character to numeric value
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
        # Convert numeric value to character
        if 0 <= digit < 10:
            return str(digit)
        if 10 <= digit < 36:
            return chr(digit - 10 + ord('a'))
        raise ValueError(f"Cannot represent digit {digit} in base {self.base}")

    def _base_to_decimal(self):
        # Convert current representation to decimal
        whole = sum(digit * (self.base ** power) 
                    for power, digit in enumerate(reversed(self.whole_digits)))
        frac = sum(digit * (self.base ** -(power+1)) 
                   for power, digit in enumerate(self.fractional_digits))
        return whole + frac * (1 if not self.negative else -1)

    def _decimal_to_base(self, decimal_value):
        # Create new AdvancedPrecisionNumber from decimal value
        new_num = AdvancedPrecisionNumber('0', self.base, self.precision)
        new_num.negative = decimal_value < 0
        decimal_value = abs(decimal_value)

        # Whole part conversion
        whole_part = int(decimal_value)
        new_num.whole_digits = []
        while whole_part > 0:
            new_num.whole_digits.insert(0, whole_part % self.base)
            whole_part //= self.base
        if not new_num.whole_digits:
            new_num.whole_digits = [0]

        # Fractional part conversion
        frac_part = decimal_value - int(decimal_value)
        new_num.fractional_digits = []
        for _ in range(self.precision):
            frac_part *= self.base
            digit = int(frac_part)
            new_num.fractional_digits.append(digit)
            frac_part -= digit

        return new_num

    def __str__(self):
        # Enhanced string representation with fraction support
        sign = '-' if self.negative else ''
        whole = ''.join(self._digit_to_char(d) for d in self.whole_digits)
        whole = whole.lstrip('0') or '0'
        
        # Trim trailing zeros from fractional part
        frac_digits = [self._digit_to_char(d) for d in self.fractional_digits]
        while frac_digits and frac_digits[-1] == '0':
            frac_digits.pop()

        # Base prefix
        base_prefix = {2: '0b', 8: '0o', 10: '', 16: '0x'}.get(self.base, f'[base{self.base}]')
    
        # Fraction representation
        if self.fraction:
            return f"{sign}{base_prefix}{whole} (Fraction: {self.fraction})"
        
        if frac_digits:
            frac = ''.join(frac_digits)
            return f"{sign}{base_prefix}{whole}.{frac}"
        return f"{sign}{base_prefix}{whole}"

    def as_fraction(self):
        """
        Convert the number to a Fraction
        """
        # If fraction is already defined, return it
        if self.fraction:
            return self.fraction if not self.negative else -self.fraction
        
        # Convert decimal representation to fraction
        decimal_value = self._base_to_decimal()
        frac = fractions.Fraction(decimal_value).limit_denominator()
        return frac if not self.negative else -frac

    def __abs__(self):
        # Create a copy without negative sign
        abs_copy = AdvancedPrecisionNumber('0', self.base, self.precision)
        abs_copy.whole_digits = self.whole_digits.copy()
        abs_copy.fractional_digits = self.fractional_digits.copy()
        return abs_copy

    def _ensure_apn(self, other):
        # Convert to AdvancedPrecisionNumber
        return other if isinstance(other, AdvancedPrecisionNumber) else \
               AdvancedPrecisionNumber(str(other), self.base, self.precision)

    def __add__(self, other):
        # Convert to decimal, add, convert back
        other = self._ensure_apn(other)
        decimal_sum = self._base_to_decimal() + other._base_to_decimal()
        
        # If both have fractions, add fractions
        if self.fraction and other.fraction:
            frac_sum = self.as_fraction() + other.as_fraction()
            result = self._decimal_to_base(float(frac_sum))
            result.fraction = frac_sum
            return result
        
        return self._decimal_to_base(decimal_sum)

    def __sub__(self, other):
        # Convert to decimal, subtract, convert back
        other = self._ensure_apn(other)
        decimal_diff = self._base_to_decimal() - other._base_to_decimal()
        
        # If both have fractions, subtract fractions
        if self.fraction and other.fraction:
            frac_diff = self.as_fraction() - other.as_fraction()
            result = self._decimal_to_base(float(frac_diff))
            result.fraction = frac_diff
            return result
        
        return self._decimal_to_base(decimal_diff)

    def __mul__(self, other):
        # Convert to decimal, multiply, convert back
        other = self._ensure_apn(other)
        decimal_product = self._base_to_decimal() * other._base_to_decimal()
        
        # If both have fractions, multiply fractions
        if self.fraction and other.fraction:
            frac_product = self.as_fraction() * other.as_fraction()
            result = self._decimal_to_base(float(frac_product))
            result.fraction = frac_product
            return result
        
        return self._decimal_to_base(decimal_product)

    def __truediv__(self, other):
        # Convert to decimal, divide, convert back
        other = self._ensure_apn(other)
        if abs(other._base_to_decimal()) < 1e-10:
            raise ZeroDivisionError("Division by zero")
        
        decimal_quotient = self._base_to_decimal() / other._base_to_decimal()
        
        # If both have fractions, divide fractions
        if self.fraction and other.fraction:
            try:
                frac_quotient = self.as_fraction() / other.as_fraction()
                result = self._decimal_to_base(float(frac_quotient))
                result.fraction = frac_quotient
                return result
            except ZeroDivisionError:
                raise ZeroDivisionError("Division by zero")
        
        return self._decimal_to_base(decimal_quotient)

    def to_fraction(self, limit_denominator=None):
        """
        Convert the number to a Fraction with optional denominator limit
        Handles various edge cases and input validations
    
        Args:
            limit_denominator (int, optional): Maximum denominator for approximation
    
        Raises:
            ValueError: For invalid input types or excessive precision
            OverflowError: For values too large to convert
        """
        # Check if limit_denominator is valid
        if limit_denominator is not None:
            if not isinstance(limit_denominator, int):
                raise ValueError("limit_denominator must be an integer")
            if limit_denominator <= 0:
                raise ValueError("limit_denominator must be a positive integer")
    
        try:
            # Convert to decimal value with error checking
            decimal_value = self._base_to_decimal()
        
            # Check for extremely large values that might cause issues
            if abs(decimal_value) > sys.float_info.max:
                raise OverflowError("Number too large to convert to fraction")
        
            # Handle very small values near zero
            if abs(decimal_value) < sys.float_info.min:
                return fractions.Fraction(0)
        
            # Perform fraction conversion
            if limit_denominator is not None:
                frac = fractions.Fraction(decimal_value).limit_denominator(limit_denominator)
            else:
                frac = fractions.Fraction(decimal_value)
        
            # Apply the sign if the number is negative
            return -frac if self.negative else frac
    
        except OverflowError:
            raise
        except Exception as e:
            raise ValueError(f"Could not convert to fraction: {e}")

    def __mod__(self, other):
        # Convert to decimal, modulo, convert back
        other = self._ensure_apn(other)
        if abs(other._base_to_decimal()) < 1e-10:
            raise ZeroDivisionError("Modulo by zero")
        
        decimal_mod = self._base_to_decimal() % other._base_to_decimal()
        return self._decimal_to_base(decimal_mod)

    def __pow__(self, other):
        # Convert to decimal, power, convert back
        other = self._ensure_apn(other)
        decimal_power = self._base_to_decimal() ** other._base_to_decimal()
        return self._decimal_to_base(decimal_power)

    def __eq__(self, other):
        other = self._ensure_apn(other)
        return abs(self._base_to_decimal() - other._base_to_decimal()) < 1e-10

    def __lt__(self, other):
        other = self._ensure_apn(other)
        return self._base_to_decimal() < other._base_to_decimal()

    def __le__(self, other):
        other = self._ensure_apn(other)
        return self._base_to_decimal() <= other._base_to_decimal()

    def __gt__(self, other):
        other = self._ensure_apn(other)
        return self._base_to_decimal() > other._base_to_decimal()

    def __ge__(self, other):
        other = self._ensure_apn(other)
        return self._base_to_decimal() >= other._base_to_decimal()

    # Unary operations
    def sqrt(self):
        return self._decimal_to_base(math.sqrt(self._base_to_decimal()))

    def sqr(self):
        return self * self

    def cube(self):
        return self * self * self

    def cube_root(self):
        return self._decimal_to_base(self._base_to_decimal() ** (1/3))

    def factorial(self):
        # Only for non-negative integers
        if self.negative or self.fractional_digits != [0] * len(self.fractional_digits):
            raise ValueError("Factorial is only defined for non-negative integers")
        
        n = int(self._base_to_decimal())
        result = math.factorial(n)
        return self._decimal_to_base(result)

    def log(self, base=None):
        """
        Calculate logarithm. 
        If base is not specified, uses natural logarithm.
        """
        if self._base_to_decimal() <= 0:
            raise ValueError("Logarithm is only defined for positive numbers")
    
        if base is None:
            # Natural logarithm
            return self._decimal_to_base(math.log(self._base_to_decimal()))
    
        # Logarithm with specified base
        base = self._ensure_apn(base)
        return self._decimal_to_base(
            math.log(self._base_to_decimal()) / math.log(base._base_to_decimal())
        )

    def inverse(self):
        """
        Calculate the multiplicative inverse (1/x)
        """
        if abs(self._base_to_decimal()) < 1e-10:
            raise ZeroDivisionError("Cannot calculate inverse of zero")
    
        return self._decimal_to_base(1 / self._base_to_decimal())

    # Trigonometric Functions
    def sin(self):
        """
        Calculate sine of the number with improved precision
        Assumes input is in radians
        Uses Taylor series expansion for more accurate results
        """
        # Convert to decimal for calculations
        x = self._base_to_decimal()
    
        # Normalize angle to [-π, π] range
        while x > math.pi:
            x -= 2 * math.pi
        while x < -math.pi:
            x += 2 * math.pi
    
        # Taylor series for sine
        # sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
        result = 0
        power = x
        factorial = 1
        sign = 1
    
        # Use enough terms for high precision
        for n in range(20):  # Increased number of terms for more precision
            if n > 0:
                factorial *= (2*n) * (2*n+1)
                power *= x * x
                sign *= -1
        
            term = sign * power / factorial
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
    
        return self._decimal_to_base(result)

    def cos(self):
        """
        Calculate cosine of the number with improved precision
        Assumes input is in radians
        Uses Taylor series expansion for more accurate results
        """
        # Convert to decimal for calculations
        x = self._base_to_decimal()
    
        # Normalize angle to [-π, π] range
        while x > math.pi:
            x -= 2 * math.pi
        while x < -math.pi:
            x += 2 * math.pi
    
        # Taylor series for cosine
        # cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
        result = 0
        power = 1
        factorial = 1
        sign = 1
    
        # Use enough terms for high precision
        for n in range(20):  # Increased number of terms for more precision
            if n > 0:
                factorial *= (2*n-1) * (2*n)
                power *= x * x
                sign *= -1
        
            term = sign * power / factorial
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
    
        return self._decimal_to_base(result)

    def tan(self):
        """
        Calculate tangent of the number with improved precision
        Assumes input is in radians
        Uses series expansion for more accurate results
        """
        # Convert to decimal for calculations
        x = self._base_to_decimal()
    
        # Normalize angle to [-π/2, π/2] range
        while x > math.pi/2:
            x -= math.pi
        while x < -math.pi/2:
            x += math.pi
    
        # Check for undefined points (where cos(x) = 0)
        if abs(math.cos(x)) < 1e-10:
            raise ValueError("Tangent is undefined at this point (cos(x) approaches zero)")
    
        # Maclaurin series for tangent
        # tan(x) = x + (1/3)x³ + (2/15)x⁵ + (17/315)x⁷ + ...
        result = 0
        power = x
    
        # Precomputed coefficients for Maclaurin series of tan(x)
        coefficients = [
            1,          # x
            1/3,        # x³
            2/15,       # x⁵
            17/315,     # x⁷
            62/2835,    # x⁹
            1382/155925,# x¹¹
            21844/6081075 # x¹³
        ]   
    
        # Compute series expansion
        for i, coeff in enumerate(coefficients):
            term = coeff * (power ** (2*i + 1))
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
        
            # Update power for next iteration
            power *= x * x
    
        return self._decimal_to_base(result)

    def arcsin(self):
        """
        Calculate arcsine (inverse sine) with improved precision
        Returns result in radians
        Uses series expansion for accurate calculation
        """
        decimal_value = self._base_to_decimal()
    
        # Input domain check
        if decimal_value < -1 or decimal_value > 1:
            raise ValueError("Arcsine is only defined for values between -1 and 1")
    
        # Special case handling for exact values
        if decimal_value == -1:
            return self._decimal_to_base(-math.pi/2)
        if decimal_value == 1:
            return self._decimal_to_base(math.pi/2)
        if decimal_value == 0:
            return self._decimal_to_base(0)
    
        # Maclaurin series for arcsin(x)
        # arcsin(x) = x + (1/2)(x³/3) + (1·3/2·4)(x⁵/5) + (1·3·5/2·4·6)(x⁷/7) + ...
        result = decimal_value
        power = decimal_value
        sign = 1
        denominator = 1
        numerator = 1
    
        # Compute series expansion
        for n in range(1, 20):  # Increased number of terms for precision
            # Update numerator and denominator for next term
            numerator *= 2 * n - 1
            denominator *= 2 * n
        
            # Compute next term in the series
            power *= decimal_value * decimal_value
            term = (numerator / (denominator * (2*n + 1))) * power
        
            # Add term to result
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
    
        return self._decimal_to_base(result)

    def arccos(self):
        """
        Calculate arccosine (inverse cosine) with improved precision
        Returns result in radians
        Uses series expansion for accurate calculation
        """
        decimal_value = self._base_to_decimal()
    
        # Input domain check
        if decimal_value < -1 or decimal_value > 1:
            raise ValueError("Arccosine is only defined for values between -1 and 1")
    
        # Special case handling for exact values
        if decimal_value == -1:
            return self._decimal_to_base(math.pi)
        if decimal_value == 1:
            return self._decimal_to_base(0)
        if decimal_value == 0:
            return self._decimal_to_base(math.pi/2)
    
        # Relationship between arcsin and arccos
        # arccos(x) = π/2 - arcsin(x)
        arcsin_value = 0
    
        # Maclaurin series for arcsin(x)
        # arcsin(x) = x + (1/2)(x³/3) + (1·3/2·4)(x⁵/5) + (1·3·5/2·4·6)(x⁷/7) + ...
        result = decimal_value
        power = decimal_value
        sign = 1
        denominator = 1
        numerator = 1
    
        # Compute series expansion
        for n in range(1, 20):  # Increased number of terms for precision
            # Update numerator and denominator for next term
            numerator *= 2 * n - 1
            denominator *= 2 * n
        
            # Compute next term in the series
            power *= decimal_value * decimal_value
            term = (numerator / (denominator * (2*n + 1))) * power
        
            # Add term to result
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
    
        # arccos(x) = π/2 - arcsin(x)
        final_result = math.pi/2 - result
    
        return self._decimal_to_base(final_result)

    def arctan(self):
        """
        Calculate arctangent (inverse tangent) with improved precision
        Returns result in radians
        Uses series expansion for accurate calculation
        """
        decimal_value = self._base_to_decimal()
    
        # Special case handling for extreme values
        if decimal_value == 0:
            return self._decimal_to_base(0)
    
        # Determine sign and work with absolute value
        sign = 1 if decimal_value > 0 else -1
        x = abs(decimal_value)
    
        # Derivative series for arctan
        # arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
        result = 0
        power = x
        sign_alternate = 1
    
        # Compute series expansion
        for n in range(20):  # Increased number of terms for precision
            # Compute term
            term = sign_alternate * (power / (2*n + 1))
            result += term
        
            # Stop if term becomes very small (suggests convergence)
            if abs(term) < 1e-15:
                break
        
            # Update for next iteration
            power *= x * x
            sign_alternate *= -1
    
        # Apply original sign
        result *= sign
    
        # Special handling for large values
        if x > 1:
            # Use the relationship: arctan(x) = π/2 - arctan(1/x) for x > 1
            result = (math.pi/2) - (sign * arctan(AdvancedPrecisionNumber('1') / AdvancedPrecisionNumber(str(x))))
    
        return self._decimal_to_base(result)

            
def calculate_repl():
    calculation_history = []

    def print_menu():
        print("\n" + "═" * 45)
        print(f"{'ADVANCED PRECISION CALCULATOR':^45}")
        print("═" * 45)
        print(f"{'OPERATION':^20}{'SYNTAX EXAMPLE':^25}")
        print("-" * 45)
        print(f"{'Addition':^20}{'4 + 5':^25}")
        print(f"{'Subtraction':^20}{'4 - 5':^25}")
        print(f"{'Multiplication':^20}{'4 * 5':^25}")
        print(f"{'Division':^20}{'4 / 5':^25}")
        print(f"{'Modulo':^20}{'4 mod 5':^25}")
        print(f"{'Percent':^20}{'4% of 5':^25}")
        print(f"{'Exponentiation':^20}{'4 ** 2':^25}")
        print(f"{'Factorial':^20}{'4! or factorial 4':^25}")
        print(f"{'Square Root':^20}{'sqrt 4':^25}")
        print(f"{'Square':^20}{'sqr 4':^25}")
        print(f"{'Cube':^20}{'cube 4':^25}")
        print(f"{'Cube Root':^20}{'cube_root 4':^25}")
        print(f"{'Reciprocal':^20}{'reciprocal 4':^25}")
        print(f"{'Logarithm':^20}{'log 4' or 'log 4 2':^25}")
        print(f"{'Inverse':^20}{'inverse 4':^25}")
        print(f"{'Base Conversion':^20}{'0b1010 or 0x10':^25}")
        print(f"{'Sine':^20}{'sin 1':^25}")
        print(f"{'Cosine':^20}{'cos 1':^25}")
        print(f"{'Tangent':^20}{'tan 1':^25}")
        print(f"{'Arcsine':^20}{'arcsin 0.5':^25}")
        print(f"{'Arccosine':^20}{'arccos 0.5':^25}")
        print(f"{'Arctangent':^20}{'arctan 1':^25}")
        print("═" * 45)
        print("Type 'menu' to show this help, 'quit' to exit")
        print("═" * 45)

    def validate_syntax(expr):
        """Validate and clean calculator input syntax"""
        # Remove extra whitespaces
        expr = ' '.join(expr.split())
        
        # Check for adjacent operators or missing spaces
        operators = ['+', '-', '*', '/', '**', 'mod', '%', 'of']
        for op in operators:
            expr = expr.replace(f'{op}', f' {op} ')
        
        # Remove duplicate spaces and strip
        expr = ' '.join(expr.split()).strip()
        
        return expr

    def perform_unary_operation(operation, expr):
        # Enhanced error handling for trigonometric functions
        try:
            num = AdvancedPrecisionNumber(expr.split()[1])
            result = getattr(num, operation)()
            print(result)
            calculation_history.append(f"{operation} {num} = {result}")
        except ValueError as e:
            print(f"Error in {operation}: {e}")
            print("Tip for trigonometric functions:")
            if operation == 'arcsin':
                print("  - Input must be between -1 and 1")
            elif operation == 'arccos':
                print("  - Input must be between -1 and 1")
            elif operation in ['sin', 'cos', 'tan', 'arctan']:
                print("  - Function expects input in radians")

    print_menu()

    while True:
        try:
            raw_expr = input(">>> ").strip().lower()
            
            if raw_expr in ['quit', 'exit', 'q']:
                break
            
            if raw_expr == 'menu':
                print_menu()
                continue
                        
            if raw_expr == 'clear':
                calculation_history.clear()
                print("Calculation history cleared.")
                continue

            # Validate and clean syntax
            expr = validate_syntax(raw_expr)

            unary_ops = {
                'factorial': 'factorial',
                '!': 'factorial',
                'sqrt': 'sqrt',
                'sqr': 'sqr',
                'cube': 'cube',
                'cube_root': 'cube_root',
                'reciprocal': 'reciprocal',
                'log': 'log',      
                'inverse': 'inverse',  
                'sin': 'sin',
                'cos': 'cos',
                'tan': 'tan',
                'arcsin': 'arcsin',
                'arccos': 'arccos',
                'arctan': 'arctan'
            }
            
            for prefix, method in unary_ops.items():
                if expr.startswith(f'{prefix} '):
                    num_expr = expr.split()[1]
                    perform_unary_operation(method, f'{prefix} {num_expr}')
                    break
            else:
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
            print("Invalid input. Type 'menu' for help.")

if __name__ == "__main__":
    calculate_repl()