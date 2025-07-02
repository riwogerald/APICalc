import fractions
import sys
import warnings

class AdvancedPrecisionNumber:
    # Predefined precision modes
    PRECISION_MODES = {
        'standard': 50,     # Default precision
        'high': 200,        # More precise calculations
        'extreme': 1000     # For scientific/mathematical computations
    }

    def __init__(self, value='0', base=10, precision_mode='standard', max_precision=1000, fraction=None):
        # Initialize basic attributes directly
        self.precision = self.PRECISION_MODES.get(precision_mode, precision_mode)
        self.max_precision = max_precision
        self.precision_loss_warning = False
        self.base = base
        self.negative = False
        self.whole_digits = [0]
        self.fractional_digits = [0] * self.precision
        self.fraction = None

        try:
            # Handle fraction input first
            if fraction is not None:
                if isinstance(fraction, (int, float, str)):
                    fraction = fractions.Fraction(fraction)
            
                if isinstance(fraction, fractions.Fraction):
                    self.fraction = fraction
                    decimal_value = float(fraction)
                    value = str(decimal_value)

            # Parse input
            if isinstance(value, AdvancedPrecisionNumber):
                self._copy_from(value)
            else:
                self._parse_input(value)

        except Exception as e:
            warnings.warn(f"Potential precision issue: {e}")
            self.precision_loss_warning = True
    
    def _copy_from(self, other):
        """Copy constructor helper"""
        self.base = other.base
        self.precision = other.precision
        self.negative = other.negative
        self.whole_digits = other.whole_digits.copy()
        self.fractional_digits = other.fractional_digits.copy()
        self.fraction = other.fraction
        self.precision_loss_warning = other.precision_loss_warning
    
    def _parse_input(self, value):
        base = 10

        if isinstance(value, AdvancedPrecisionNumber):
            self._copy_from(value)
            return

        if isinstance(value, (int, float)):
            value = str(value)

        if isinstance(value, str):
            value = value.strip().lower()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Base detection
            if value.startswith('0b'):
                base = 2
                value = value[2:]
            elif value.startswith('0x'):
                base = 16
                value = value[2:]
            elif value.startswith('0o'):
                base = 8
                value = value[2:]
        
            self.base = base

            # Handle scientific notation
            if 'e' in value:
                parts = value.split('e')
                if len(parts) == 2:
                    mantissa = float(parts[0])
                    exponent = int(parts[1])
                    value = str(mantissa * (10 ** exponent))

            parts = value.split('.')
            whole = parts[0] or '0'
            fractional = parts[1] if len(parts) > 1 else ''

            whole_digits = [self._char_to_digit(c) for c in whole.replace('_', '') if c.isalnum()]
            frac_digits = [self._char_to_digit(c) for c in fractional.replace('_', '') if c.isalnum()]
        
            if len(whole_digits) > self.precision or len(frac_digits) > self.precision:
                warnings.warn(f"Input exceeds current precision: {len(whole_digits)} whole digits, {len(frac_digits)} fractional digits")
                self._increase_precision()

            self.whole_digits = whole_digits if whole_digits else [0]
            self.fractional_digits = frac_digits[:self.precision]
        
            while len(self.fractional_digits) < self.precision:
                self.fractional_digits.append(0)

    def _increase_precision(self):
        new_precision = min(self.precision * 2, self.max_precision)
        if new_precision > self.precision:
            self.precision = new_precision
            self.fractional_digits.extend([0] * (new_precision - len(self.fractional_digits)))
            self.precision_loss_warning = True

    def _check_numeric_limits(self, value):
        """Enhanced numeric limit checking"""
        if abs(value) > sys.float_info.max:
            warnings.warn("Number exceeds maximum representable value")
            self._increase_precision()
        
        if 0 < abs(value) < sys.float_info.min:
            warnings.warn("Number is extremely close to zero, precision may be compromised")

    def _char_to_digit(self, char):
        if char.isdigit():
            digit = int(char)
            if digit >= self.base:
                raise ValueError(f"Digit {digit} not valid in base {self.base}")
            return digit
        
        if char.isalpha():
            digit = ord(char.lower()) - ord('a') + 10
            if digit >= self.base:
                raise ValueError(f"Digit {char} not valid in base {self.base}")
            return digit
        
        raise ValueError(f"Invalid character {char}")

    def _digit_to_char(self, digit):
        if 0 <= digit < 10:
            return str(digit)
        if 10 <= digit < 36:
            return chr(digit - 10 + ord('a'))
        raise ValueError(f"Cannot represent digit {digit} in base {self.base}")
    
    def _abs_compare(self, other):
        if len(self.whole_digits) != len(other.whole_digits):
            return len(self.whole_digits) - len(other.whole_digits)
        
        for d1, d2 in zip(self.whole_digits, other.whole_digits):
            if d1 != d2:
                return d1 - d2
        
        for d1, d2 in zip(self.fractional_digits, other.fractional_digits):
            if d1 != d2:
                return d1 - d2
        
        return 0
          
    def _base_to_decimal(self):
        # Reimplemented to maintain higher precision
        whole = sum(digit * (self.base ** power) 
                    for power, digit in enumerate(reversed(self.whole_digits)))
        frac = sum(digit * (self.base ** -(power+1)) 
                   for power, digit in enumerate(self.fractional_digits))
        total = whole + frac
        return -total if self.negative else total

    def _decimal_to_base(self, decimal_value, preserve_sign=True):
        new_num = AdvancedPrecisionNumber('0', self.base, self.precision)
    
        # Preserve sign
        if preserve_sign:
            new_num.negative = decimal_value < 0
        decimal_value = abs(decimal_value)

        # Whole part conversion (more precise)
        whole_part = int(decimal_value)
        new_num.whole_digits = []
        while whole_part > 0:
            new_num.whole_digits.insert(0, whole_part % self.base)
            whole_part //= self.base
        if not new_num.whole_digits:
            new_num.whole_digits = [0]

        # Fractional part conversion (improved)
        frac_part = decimal_value - int(decimal_value)
        new_num.fractional_digits = []
        for _ in range(self.precision):
            frac_part *= self.base
            digit = int(frac_part)
            new_num.fractional_digits.append(digit)
            frac_part -= digit

        return new_num
    
    def _convert_to_base(self, new_base):
        """Convert number to a different base"""
        decimal_value = self._base_to_decimal()
        result = AdvancedPrecisionNumber('0', new_base, self.precision)
        result.negative = self.negative
        
        # Convert whole part
        whole_part = int(abs(decimal_value))
        result.whole_digits = []
        while whole_part > 0:
            result.whole_digits.insert(0, whole_part % new_base)
            whole_part //= new_base
        if not result.whole_digits:
            result.whole_digits = [0]
        
        # Convert fractional part
        frac_part = abs(decimal_value) - int(abs(decimal_value))
        result.fractional_digits = []
        for _ in range(self.precision):
            frac_part *= new_base
            digit = int(frac_part)
            result.fractional_digits.append(digit)
            frac_part -= digit
        
        return result
    
    def _is_zero(self):
        return all(d == 0 for d in self.whole_digits) and all(d == 0 for d in self.fractional_digits)

    def _abs_value_as_digits(self):
        return self.whole_digits + self.fractional_digits

    def __str__(self):
        """Enhanced string representation with precision warning and fraction support"""
        # Determine sign
        sign = '-' if self.negative else ''
    
        # Convert whole digits to string
        whole = ''.join(self._digit_to_char(d) for d in self.whole_digits)
        whole = whole.lstrip('0') or '0'
    
        # Trim trailing zeros from fractional part
        frac_digits = [self._digit_to_char(d) for d in self.fractional_digits]
        while frac_digits and frac_digits[-1] == '0':
            frac_digits.pop()

        # Base prefix
        base_prefix = {2: '0b', 8: '0o', 10: '', 16: '0x'}.get(self.base, f'[base{self.base}]')
    
        # Fraction representation takes precedence
        if self.fraction:
            return f"{sign}{base_prefix}{whole} (Fraction: {self.fraction})"
    
        # Standard representation with optional fractional part
        if frac_digits:
            frac = ''.join(frac_digits)
            result = f"{sign}{base_prefix}{whole}.{frac}"
        else:
            result = f"{sign}{base_prefix}{whole}"
    
        # Append precision warning if applicable
        if self.precision_loss_warning:
            result += " [PRECISION WARNING]"
    
        return result

    def __repr__(self):
        return f"AdvancedPrecisionNumber('{str(self)}')"

    def __hash__(self):
        """Make the object hashable"""
        return hash((tuple(self.whole_digits), tuple(self.fractional_digits), self.negative, self.base))

    def __format__(self, format_spec):
        """Support for format() function"""
        if format_spec.endswith('f'):
            # Handle floating point format
            try:
                precision = int(format_spec[:-1].split('.')[1]) if '.' in format_spec else 6
                decimal_val = self._base_to_decimal()
                return f"{decimal_val:.{precision}f}"
            except:
                return str(self)
        return str(self)

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
        """Add two numbers in their native base without conversion"""
        other = self._ensure_apn(other)
    
        # Handle different bases by converting other to self's base
        if other.base != self.base:
            other = other._convert_to_base(self.base)
    
        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
    
        # Handle signs
        if self.negative == other.negative:
            result = self._abs_add(other)
            result.negative = self.negative
        else:
            # If signs differ, subtract absolute values
            if self._abs_compare(other) >= 0:
                result = self._abs_subtract(other)
                result.negative = self.negative
            else:
                result = other._abs_subtract(self)
                result.negative = other.negative
    
        return result

    def _abs_add(self, other):
        """Add absolute values directly in base"""
        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
        carry = 0
    
        # Add fractional parts from right to left
        max_frac_len = max(len(self.fractional_digits), len(other.fractional_digits))
        result.fractional_digits = [0] * max_frac_len
        
        for i in range(max_frac_len - 1, -1, -1):
            digit1 = self.fractional_digits[i] if i < len(self.fractional_digits) else 0
            digit2 = other.fractional_digits[i] if i < len(other.fractional_digits) else 0
        
            # Add in current base
            total = digit1 + digit2 + carry
            result.fractional_digits[i] = total % self.base
            carry = total // self.base
    
        # Add whole parts from right to left
        whole1 = self.whole_digits[::-1]
        whole2 = other.whole_digits[::-1]
        result_whole = []
    
        for i in range(max(len(whole1), len(whole2))):
            digit1 = whole1[i] if i < len(whole1) else 0
            digit2 = whole2[i] if i < len(whole2) else 0
        
            # Add in current base
            total = digit1 + digit2 + carry
            result_whole.append(total % self.base)
            carry = total // self.base
    
        if carry:
            result_whole.append(carry)
    
        result.whole_digits = result_whole[::-1]
        return result

    def __sub__(self, other):
        """Subtract two numbers in their native base without conversion"""
        other = self._ensure_apn(other)
    
        if other.base != self.base:
            other = other._convert_to_base(self.base)
    
        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
    
        # If signs are different, add absolute values
        if self.negative != other.negative:
            result = self._abs_add(other)
            result.negative = self.negative
            return result
    
        # If signs are same, subtract absolute values
        if self._abs_compare(other) >= 0:
            result = self._abs_subtract(other)
            result.negative = self.negative
        else:
            result = other._abs_subtract(self)
            result.negative = not self.negative
    
        return result

    def _abs_subtract(self, other):
        """Subtract absolute values directly in base"""
        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
        borrow = 0
    
        # Ensure both have same fractional length
        max_frac_len = max(len(self.fractional_digits), len(other.fractional_digits))
        result.fractional_digits = [0] * max_frac_len
        
        # Subtract fractional parts
        for i in range(max_frac_len - 1, -1, -1):
            digit1 = self.fractional_digits[i] if i < len(self.fractional_digits) else 0
            digit2 = other.fractional_digits[i] if i < len(other.fractional_digits) else 0
        
            # Handle borrow
            if digit1 < digit2 + borrow:
                digit1 += self.base
                result.fractional_digits[i] = digit1 - digit2 - borrow
                borrow = 1
            else:
                result.fractional_digits[i] = digit1 - digit2 - borrow
                borrow = 0
    
        # Subtract whole parts
        whole1 = self.whole_digits[::-1]
        whole2 = other.whole_digits[::-1]
        result_whole = []
    
        for i in range(max(len(whole1), len(whole2))):
            digit1 = whole1[i] if i < len(whole1) else 0
            digit2 = whole2[i] if i < len(whole2) else 0
        
            if digit1 < digit2 + borrow:
                digit1 += self.base
                result_whole.append(digit1 - digit2 - borrow)
                borrow = 1
            else:
                result_whole.append(digit1 - digit2 - borrow)
                borrow = 0
    
        result.whole_digits = result_whole[::-1]
    
        # Remove leading zeros
        while len(result.whole_digits) > 1 and result.whole_digits[0] == 0:
            result.whole_digits.pop(0)
    
        return result
   
    def __mul__(self, other):
        """Multiply two numbers directly in their base without conversion"""
        other = self._ensure_apn(other)

        # Handle different bases
        if other.base != self.base:
            other = other._convert_to_base(self.base)

        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
        result.negative = self.negative != other.negative

        # Use Karatsuba for large numbers
        if len(self.whole_digits) > 32 and len(other.whole_digits) > 32:
            return self._karatsuba_multiply(other)

        # Regular multiplication for smaller numbers
        return self._standard_multiply(other)

    def _standard_multiply(self, other):
        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
        result.negative = self.negative != other.negative

        # Convert to single digit arrays for easier multiplication
        self_digits = self.whole_digits + self.fractional_digits
        other_digits = other.whole_digits + other.fractional_digits
        
        # Calculate total fractional positions
        self_frac_pos = len(self.fractional_digits)
        other_frac_pos = len(other.fractional_digits)
        total_frac_pos = self_frac_pos + other_frac_pos
        
        # Multiply digit arrays
        product = [0] * (len(self_digits) + len(other_digits))
        
        for i in range(len(self_digits) - 1, -1, -1):
            carry = 0
            for j in range(len(other_digits) - 1, -1, -1):
                pos = i + j + 1
                temp = product[pos] + self_digits[i] * other_digits[j] + carry
                product[pos] = temp % self.base
                carry = temp // self.base
            if carry:
                product[i] += carry

        # Remove leading zeros
        while len(product) > 1 and product[0] == 0:
            product.pop(0)

        # Split back into whole and fractional parts
        if total_frac_pos >= len(product):
            # Result is purely fractional
            result.whole_digits = [0]
            result.fractional_digits = ([0] * (total_frac_pos - len(product)) + product)[:result.precision]
        else:
            # Split normally
            split_pos = len(product) - total_frac_pos
            result.whole_digits = product[:split_pos] if split_pos > 0 else [0]
            result.fractional_digits = (product[split_pos:] + [0] * result.precision)[:result.precision]

        return result

    def _karatsuba_multiply(self, other):
        """Karatsuba multiplication algorithm for large numbers"""
        if len(self.whole_digits) <= 32 or len(other.whole_digits) <= 32:
            return self._standard_multiply(other)

        # Split numbers into high and low parts
        m = max(len(self.whole_digits), len(other.whole_digits))
        m2 = m // 2

        # Split self into high and low
        high1 = AdvancedPrecisionNumber('0', self.base)
        low1 = AdvancedPrecisionNumber('0', self.base)
        high1.whole_digits = self.whole_digits[:-m2] if len(self.whole_digits) > m2 else [0]
        low1.whole_digits = self.whole_digits[-m2:]

        # Split other into high and low
        high2 = AdvancedPrecisionNumber('0', self.base)
        low2 = AdvancedPrecisionNumber('0', self.base)
        high2.whole_digits = other.whole_digits[:-m2] if len(other.whole_digits) > m2 else [0]
        low2.whole_digits = other.whole_digits[-m2:]

        # Recursive steps
        z0 = low1._standard_multiply(low2)
        z1 = (high1 + low1)._standard_multiply(high2 + low2) - high1._standard_multiply(high2) - z0
        z2 = high1._standard_multiply(high2)

        # Combine results
        result = z2
        for _ in range(2 * m2):
            result.whole_digits.append(0)
    
        temp = z1
        for _ in range(m2):
            temp.whole_digits.append(0)
    
        result = result + temp + z0
        result.negative = self.negative != other.negative

        return result

    def __truediv__(self, other):
        """Divide two numbers directly in their base without conversion"""
        other = self._ensure_apn(other)

        if other._is_zero():
            raise ZeroDivisionError("Division by zero")

        if other.base != self.base:
            other = other._convert_to_base(self.base)

        # Handle signs
        result_negative = self.negative != other.negative
    
        # Use Newton-Raphson for optimization if numbers are large
        if len(self.whole_digits) > 50 or len(other.whole_digits) > 50:
            return self._newton_raphson_divide(other)

        return self._long_division(other, result_negative)

    def _long_division(self, other, result_negative):
        precision = max(self.precision, other.precision)
        result = AdvancedPrecisionNumber('0', self.base, precision)
        result.negative = result_negative

        # Convert to integers for division
        self_int = 0
        for digit in self.whole_digits:
            self_int = self_int * self.base + digit
        for digit in self.fractional_digits:
            self_int = self_int * self.base + digit

        other_int = 0
        for digit in other.whole_digits:
            other_int = other_int * self.base + digit
        for digit in other.fractional_digits:
            other_int = other_int * self.base + digit

        if other_int == 0:
            raise ZeroDivisionError("Division by zero")

        # Perform division
        quotient = self_int // other_int
        remainder = self_int % other_int

        # Convert back to base representation
        result.whole_digits = []
        temp = quotient
        while temp > 0:
            result.whole_digits.insert(0, temp % self.base)
            temp //= self.base

        if not result.whole_digits:
            result.whole_digits = [0]

        # Calculate fractional part
        result.fractional_digits = []
        for _ in range(precision):
            remainder *= self.base
            digit = remainder // other_int
            result.fractional_digits.append(digit)
            remainder = remainder % other_int

        return result

    def _newton_raphson_divide(self, other):
        """Division using Newton-Raphson method for optimization"""
        precision = max(self.precision, other.precision)
        result = AdvancedPrecisionNumber('0', self.base, precision)
    
        # Initial guess (using shift operations in the current base)
        x = self._initial_guess_for_division(other)
    
        # Newton iterations: x = x * (2 - other * x)
        for _ in range(10):  # Usually converges in fewer iterations
            prev_x = x
            x = x * (AdvancedPrecisionNumber('2', self.base) - other * x)
        
            # Check for convergence
            if abs(float(x._base_to_decimal()) - float(prev_x._base_to_decimal())) < 1e-10:
                break
    
        # Final multiplication to get result
        result = self * x
        result.negative = self.negative != other.negative
    
        return result
    
    def _initial_guess_for_division(self, other):
        # Simple initial guess for Newton-Raphson division
        return AdvancedPrecisionNumber('1', self.base, self.precision)

    def __mod__(self, other):
        # Convert to decimal, modulo, convert back
        other = self._ensure_apn(other)
        if other._is_zero():
            raise ZeroDivisionError("Modulo by zero")
        
        # Perform division and get remainder
        quotient = self // other
        remainder = self - (quotient * other)
        return remainder

    def __floordiv__(self, other):
        """Floor division"""
        result = self / other
        # Floor the result
        result.fractional_digits = [0] * result.precision
        return result

    def __pow__(self, n):
        """Calculate power using binary exponentiation in current base"""
        if isinstance(n, AdvancedPrecisionNumber):
            n = int(n._base_to_decimal())
        
        if not isinstance(n, int):
            raise ValueError("Power operation currently supports only integer exponents")
    
        if n == 0:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
    
        if n < 0:
            base_inv = self.inverse()
            return base_inv.__pow__(-n)
    
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        base = AdvancedPrecisionNumber(str(self), self.base, self.precision)
    
        while n > 0:
            if n & 1:  # If n is odd
                result = result * base
            base = base * base
            n >>= 1
    
        return result

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

    def __ne__(self, other):
        return not self.__eq__(other)

    # Unary operations
    def sqrt(self):
        """Calculate square root directly in base using Newton's method"""
        if self.negative:
            raise ValueError("Cannot calculate square root of negative number")
        
        if self._is_zero():
            return AdvancedPrecisionNumber('0', self.base, self.precision)

        # Use Newton's method for square root: x_{n+1} = (x_n + a/x_n) / 2
        x = AdvancedPrecisionNumber('1', self.base, self.precision)
        two = AdvancedPrecisionNumber('2', self.base, self.precision)
        
        for _ in range(max(50, self.precision)):
            prev_x = x
            try:
                x = (x + self / x) / two
                
                # Check for convergence
                if abs(x._base_to_decimal() - prev_x._base_to_decimal()) < 1e-15:
                    break
            except:
                break
        
        return x

    def sqr(self):
        return self * self

    def cube(self):
        return self * self * self

    def cube_root(self):
        """Calculate cube root using Newton's method"""
        if self._is_zero():
            return AdvancedPrecisionNumber('0', self.base, self.precision)
        
        x = AdvancedPrecisionNumber('1', self.base, self.precision)
        three = AdvancedPrecisionNumber('3', self.base, self.precision)
        
        for _ in range(self.precision):
            prev_x = x
            x_squared = x * x
            x = (AdvancedPrecisionNumber('2', self.base) * x + self / x_squared) / three
            
            if abs(x._base_to_decimal() - prev_x._base_to_decimal()) < 1e-15:
                break
        
        return x

    def factorial(self):
        """Calculate factorial for non-negative integers"""
        # Only for non-negative integers
        if self.negative or any(d != 0 for d in self.fractional_digits):
            raise ValueError("Factorial is only defined for non-negative integers")
    
        # Convert to integer value
        n = int(self._base_to_decimal())
    
        # Handle special cases
        if n == 0 or n == 1:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
    
        # Iterative factorial calculation
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        for i in range(2, n + 1):
            result = result * AdvancedPrecisionNumber(str(i), self.base, self.precision)
    
        return result

    def log(self, base=None):
        """Calculate natural logarithm or logarithm with specified base"""
        if self.negative or self._is_zero():
            raise ValueError("Logarithm undefined for non-positive numbers")

        if base is not None:
            base_num = self._ensure_apn(base)
            if base_num._is_zero() or base_num.negative:
                raise ValueError("Logarithm base must be positive")
            
            if base_num == AdvancedPrecisionNumber('1', self.base):
                raise ValueError("Logarithm base cannot be 1")

        # For now, use built-in math.log and convert back
        import math
        decimal_val = self._base_to_decimal()
        
        if base is not None:
            base_val = base_num._base_to_decimal()
            log_result = math.log(decimal_val, base_val)
        else:
            log_result = math.log(decimal_val)
        
        return AdvancedPrecisionNumber(str(log_result), self.base, self.precision)

    def exp(self):
        """Calculate exponential function"""
        import math
        decimal_val = self._base_to_decimal()
        exp_result = math.exp(decimal_val)
        return AdvancedPrecisionNumber(str(exp_result), self.base, self.precision)

    def inverse(self):
        """Calculate multiplicative inverse (1/x)"""
        if self._is_zero():
            raise ZeroDivisionError("Cannot calculate inverse of zero")
        
        one = AdvancedPrecisionNumber('1', self.base, self.precision)
        return one / self

    # Trigonometric Functions
    def sin(self):
        """Calculate sine"""
        import math
        decimal_val = self._base_to_decimal()
        sin_result = math.sin(decimal_val)
        return AdvancedPrecisionNumber(str(sin_result), self.base, self.precision)

    def cos(self):
        """Calculate cosine"""
        import math
        decimal_val = self._base_to_decimal()
        cos_result = math.cos(decimal_val)
        return AdvancedPrecisionNumber(str(cos_result), self.base, self.precision)

    def tan(self):
        """Calculate tangent"""
        import math
        decimal_val = self._base_to_decimal()
        tan_result = math.tan(decimal_val)
        return AdvancedPrecisionNumber(str(tan_result), self.base, self.precision)

    def arcsin(self):
        """Calculate arcsine"""
        import math
        decimal_val = self._base_to_decimal()
        if abs(decimal_val) > 1:
            raise ValueError("Arcsine argument must be between -1 and 1")
        arcsin_result = math.asin(decimal_val)
        return AdvancedPrecisionNumber(str(arcsin_result), self.base, self.precision)

    def arccos(self):
        """Calculate arccosine"""
        import math
        decimal_val = self._base_to_decimal()
        if abs(decimal_val) > 1:
            raise ValueError("Arccosine argument must be between -1 and 1")
        arccos_result = math.acos(decimal_val)
        return AdvancedPrecisionNumber(str(arccos_result), self.base, self.precision)

    def arctan(self):
        """Calculate arctangent"""
        import math
        decimal_val = self._base_to_decimal()
        arctan_result = math.atan(decimal_val)
        return AdvancedPrecisionNumber(str(arctan_result), self.base, self.precision)

    def to_fraction(self, limit_denominator=None):
        """Convert the number to a Fraction with optional denominator limit"""
        if limit_denominator is not None:
            if not isinstance(limit_denominator, int):
                raise ValueError("limit_denominator must be an integer")
            if limit_denominator <= 0:
                raise ValueError("limit_denominator must be a positive integer")
    
        try:
            decimal_value = self._base_to_decimal()
        
            if abs(decimal_value) > sys.float_info.max:
                raise OverflowError("Number too large to convert to fraction")
        
            if abs(decimal_value) < sys.float_info.min:
                return fractions.Fraction(0)
        
            if limit_denominator is not None:
                frac = fractions.Fraction(decimal_value).limit_denominator(limit_denominator)
            else:
                frac = fractions.Fraction(decimal_value)
        
            return -frac if self.negative else frac
    
        except OverflowError:
            raise
        except Exception as e:
            raise ValueError(f"Could not convert to fraction: {e}")

            
def calculate_repl():
    """Enhanced REPL calculator with better error handling and features"""
    calculation_history = []

    def print_menu():
        print("\n" + "═" * 60)
        print(f"{'ADVANCED PRECISION CALCULATOR':^60}")
        print("═" * 60)
        print(f"{'OPERATION':^25}{'SYNTAX EXAMPLE':^35}")
        print("-" * 60)
        print(f"{'Addition':^25}{'4 + 5':^35}")
        print(f"{'Subtraction':^25}{'4 - 5':^35}")
        print(f"{'Multiplication':^25}{'4 * 5':^35}")
        print(f"{'Division':^25}{'4 / 5':^35}")
        print(f"{'Floor Division':^25}{'4 // 5':^35}")
        print(f"{'Modulo':^25}{'4 % 5':^35}")
        print(f"{'Exponentiation':^25}{'4 ** 2':^35}")
        print(f"{'Factorial':^25}{'factorial(4) or 4!':^35}")
        print(f"{'Square Root':^25}{'sqrt(4)':^35}")
        print(f"{'Square':^25}{'sqr(4)':^35}")
        print(f"{'Cube':^25}{'cube(4)':^35}")
        print(f"{'Cube Root':^25}{'cube_root(4)':^35}")
        print(f"{'Reciprocal':^25}{'inverse(4)':^35}")
        print(f"{'Logarithm':^25}{'log(4) or log(4, 2)':^35}")
        print(f"{'Base Conversion':^25}{'0b1010 or 0x10':^35}")
        print(f"{'Trigonometric':^25}{'sin(1), cos(1), tan(1)':^35}")
        print(f"{'Inverse Trig':^25}{'arcsin(0.5), arccos(0.5)':^35}")
        print(f"{'Fractions':^25}{'to_fraction()':^35}")
        print("═" * 60)
        print("Commands: 'menu' (help), 'history' (show history), 'clear' (clear history), 'quit' (exit)")
        print("═" * 60)

    def safe_eval(expr):
        """Safely evaluate mathematical expressions"""
        # Replace function calls with method calls
        expr = expr.replace('factorial(', 'TEMP.factorial() if TEMP == ')
        expr = expr.replace('sqrt(', 'TEMP.sqrt() if TEMP == ')
        expr = expr.replace('sqr(', 'TEMP.sqr() if TEMP == ')
        expr = expr.replace('cube(', 'TEMP.cube() if TEMP == ')
        expr = expr.replace('cube_root(', 'TEMP.cube_root() if TEMP == ')
        expr = expr.replace('inverse(', 'TEMP.inverse() if TEMP == ')
        expr = expr.replace('sin(', 'TEMP.sin() if TEMP == ')
        expr = expr.replace('cos(', 'TEMP.cos() if TEMP == ')
        expr = expr.replace('tan(', 'TEMP.tan() if TEMP == ')
        expr = expr.replace('arcsin(', 'TEMP.arcsin() if TEMP == ')
        expr = expr.replace('arccos(', 'TEMP.arccos() if TEMP == ')
        expr = expr.replace('arctan(', 'TEMP.arctan() if TEMP == ')
        expr = expr.replace('log(', 'TEMP.log() if TEMP == ')
        
        # Handle simple expressions
        try:
            # Split by operators and convert to AdvancedPrecisionNumber
            tokens = []
            current_token = ""
            operators = ['+', '-', '*', '/', '%', '(', ')', '**', '//', '!']
            
            i = 0
            while i < len(expr):
                char = expr[i]
                
                # Handle multi-character operators
                if i < len(expr) - 1:
                    two_char = expr[i:i+2]
                    if two_char in ['**', '//']:
                        if current_token:
                            tokens.append(current_token.strip())
                            current_token = ""
                        tokens.append(two_char)
                        i += 2
                        continue
                
                if char in operators:
                    if current_token:
                        tokens.append(current_token.strip())
                        current_token = ""
                    tokens.append(char)
                else:
                    current_token += char
                
                i += 1
            
            if current_token:
                tokens.append(current_token.strip())
            
            # Convert numeric tokens to AdvancedPrecisionNumber
            for i, token in enumerate(tokens):
                if token not in operators and token.strip():
                    try:
                        tokens[i] = AdvancedPrecisionNumber(token)
                    except:
                        pass  # Keep as string if conversion fails
            
            return tokens
            
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    def evaluate_expression(tokens):
        """Evaluate tokenized expression"""
        if len(tokens) == 1:
            return tokens[0]
        
        # Handle factorial first
        i = 0
        while i < len(tokens):
            if tokens[i] == '!':
                if i > 0:
                    result = tokens[i-1].factorial()
                    tokens = tokens[:i-1] + [result] + tokens[i+1:]
                    i -= 1
                else:
                    raise ValueError("Invalid factorial usage")
            i += 1
        
        # Handle exponentiation
        i = 0
        while i < len(tokens):
            if tokens[i] == '**':
                if i > 0 and i < len(tokens) - 1:
                    result = tokens[i-1] ** tokens[i+1]
                    tokens = tokens[:i-1] + [result] + tokens[i+2:]
                    i -= 1
                else:
                    raise ValueError("Invalid exponentiation")
            i += 1
        
        # Handle multiplication, division, modulo
        i = 0
        while i < len(tokens):
            if tokens[i] in ['*', '/', '//', '%']:
                if i > 0 and i < len(tokens) - 1:
                    if tokens[i] == '*':
                        result = tokens[i-1] * tokens[i+1]
                    elif tokens[i] == '/':
                        result = tokens[i-1] / tokens[i+1]
                    elif tokens[i] == '//':
                        result = tokens[i-1] // tokens[i+1]
                    elif tokens[i] == '%':
                        result = tokens[i-1] % tokens[i+1]
                    
                    tokens = tokens[:i-1] + [result] + tokens[i+2:]
                    i -= 1
                else:
                    raise ValueError(f"Invalid {tokens[i]} operation")
            i += 1
        
        # Handle addition and subtraction
        i = 0
        while i < len(tokens):
            if tokens[i] in ['+', '-']:
                if i > 0 and i < len(tokens) - 1:
                    if tokens[i] == '+':
                        result = tokens[i-1] + tokens[i+1]
                    elif tokens[i] == '-':
                        result = tokens[i-1] - tokens[i+1]
                    
                    tokens = tokens[:i-1] + [result] + tokens[i+2:]
                    i -= 1
                else:
                    raise ValueError(f"Invalid {tokens[i]} operation")
            i += 1
        
        if len(tokens) == 1:
            return tokens[0]
        else:
            raise ValueError("Could not evaluate expression")

    print_menu()

    while True:
        try:
            raw_expr = input(">>> ").strip()
            
            if raw_expr.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if raw_expr.lower() == 'menu':
                print_menu()
                continue
            
            if raw_expr.lower() == 'history':
                if calculation_history:
                    print("\nCalculation History:")
                    for i, calc in enumerate(calculation_history[-10:], 1):  # Show last 10
                        print(f"{i:2d}. {calc}")
                else:
                    print("No calculation history.")
                continue
                        
            if raw_expr.lower() == 'clear':
                calculation_history.clear()
                print("Calculation history cleared.")
                continue

            if not raw_expr:
                continue

            # Handle function calls
            if any(func in raw_expr for func in ['factorial(', 'sqrt(', 'sin(', 'cos(', 'tan(', 'log(']):
                # Extract function and argument
                for func_name in ['factorial', 'sqrt', 'sqr', 'cube', 'cube_root', 'inverse', 
                                  'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'log']:
                    if f'{func_name}(' in raw_expr:
                        start = raw_expr.find(f'{func_name}(') + len(func_name) + 1
                        end = raw_expr.find(')', start)
                        if end != -1:
                            arg = raw_expr[start:end].strip()
                            
                            # Handle log with base
                            if func_name == 'log' and ',' in arg:
                                args = [a.strip() for a in arg.split(',')]
                                num = AdvancedPrecisionNumber(args[0])
                                base = AdvancedPrecisionNumber(args[1])
                                result = num.log(base)
                            else:
                                num = AdvancedPrecisionNumber(arg)
                                result = getattr(num, func_name)()
                            
                            print(result)
                            calculation_history.append(f"{raw_expr} = {result}")
                            break
                continue

            # Handle simple expressions
            try:
                tokens = safe_eval(raw_expr)
                result = evaluate_expression(tokens)
                print(result)
                calculation_history.append(f"{raw_expr} = {result}")
            except Exception as e:
                # Try to parse as single number
                try:
                    result = AdvancedPrecisionNumber(raw_expr)
                    print(result)
                    calculation_history.append(f"{raw_expr}")
                except:
                    print(f"Error: {e}")
                    print("Type 'menu' for help with syntax.")
        
        except KeyboardInterrupt:
            print("\nUse 'quit' to exit.")
        except Exception as e:
            print(f"Error: {e}")
            print("Type 'menu' for help.")

if __name__ == "__main__":
    calculate_repl()