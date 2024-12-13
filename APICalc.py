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
    
    def _parse_input(self, value):
        base = 10

        if isinstance(value, AdvancedPrecisionNumber):
            self.base = value.base
            self.precision = value.precision
            self.negative = value.negative
            self.whole_digits = value.whole_digits.copy()
            self.fractional_digits = value.fractional_digits.copy()
            return

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

            parts = value.split('.')
            whole = parts[0] or '0'
            fractional = parts[1] if len(parts) > 1 else ''

            whole_digits = [self._char_to_digit(c) for c in whole.replace('_', '')]
            frac_digits = [self._char_to_digit(c) for c in fractional.replace('_', '')]
        
            if len(whole_digits) > self.precision or len(frac_digits) > self.precision:
                warnings.warn(f"Input exceeds current precision: {len(whole_digits)} whole digits, {len(frac_digits)} fractional digits")
                self._increase_precision()

            self.whole_digits = whole_digits
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
        
        digit = ord(char.lower()) - ord('a') + 10
        if digit >= self.base:
            raise ValueError(f"Digit {char} not valid in base {self.base}")
        return digit

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
            result.negative = self.negative
            result = self._abs_add(other)
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
        for i in range(max(len(self.fractional_digits), len(other.fractional_digits)) - 1, -1, -1):
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
    
        # Subtract fractional parts
        for i in range(len(self.fractional_digits) - 1, -1, -1):
            digit1 = self.fractional_digits[i]
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

        # Separate handling for whole and fractional parts
        whole_product = [0] * (len(self.whole_digits) + len(other.whole_digits))
    
        # Multiply whole parts
        for i in range(len(self.whole_digits)-1, -1, -1):
            carry = 0
            for j in range(len(other.whole_digits)-1, -1, -1):
                pos = i + j
                temp = whole_product[pos] + self.whole_digits[i] * other.whole_digits[j] + carry
                whole_product[pos] = temp % self.base
                carry = temp // self.base
            if carry:
                whole_product[i-1] = carry

        # Remove leading zeros from whole part
        while len(whole_product) > 1 and whole_product[0] == 0:
            whole_product.pop(0)

        # Handle fractional parts if present
        frac_len = len(self.fractional_digits) + len(other.fractional_digits)
        frac_product = [0] * frac_len

        if frac_len > 0:
            # Multiply including fractional parts
            all_digits1 = self.whole_digits + self.fractional_digits
            all_digits2 = other.whole_digits + other.fractional_digits
        
            for i in range(len(all_digits1)-1, -1, -1):
                carry = 0
                for j in range(len(all_digits2)-1, -1, -1):
                    pos = i + j - frac_len
                    if 0 <= pos < len(frac_product):
                        temp = frac_product[pos] + all_digits1[i] * all_digits2[j] + carry
                        frac_product[pos] = temp % self.base
                        carry = temp // self.base

        # Set results
        result.whole_digits = whole_product
        result.fractional_digits = (frac_product + [0] * result.precision)[:result.precision]

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
        z1 = (high1._standard_multiply(low2))._abs_add(low1._standard_multiply(high2))
        z2 = high1._standard_multiply(high2)

        # Combine results
        result = z2
        for _ in range(2 * m2):
            result.whole_digits.append(0)
    
        temp = z1
        for _ in range(m2):
            temp.whole_digits.append(0)
    
        result = result._abs_add(temp)._abs_add(z0)
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

        # Scale the dividend and divisor
        scale = self.base ** precision
        dividend = int(''.join(map(str, self.whole_digits))) * scale + \
                int(''.join(map(str, self.fractional_digits[:precision])))
        divisor = int(''.join(map(str, other.whole_digits))) * scale + \
                int(''.join(map(str, other.fractional_digits[:precision])))

        if divisor == 0:
            raise ZeroDivisionError("Division by zero")

        # Perform division
        quotient = dividend // divisor
        remainder = dividend % divisor

        # Convert back to base representation
        whole_part = quotient
        result.whole_digits = []
        while whole_part > 0:
            result.whole_digits.insert(0, whole_part % self.base)
            whole_part //= self.base

        if not result.whole_digits:
            result.whole_digits = [0]

        # Calculate fractional part
        frac_part = remainder / divisor
        result.fractional_digits = []
        for _ in range(precision):
            frac_part *= self.base
            digit = int(frac_part)
            result.fractional_digits.append(digit)
            frac_part -= digit

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
            x = x._standard_multiply(
                AdvancedPrecisionNumber('2', self.base) - 
                other._standard_multiply(x)
            )
        
            # Check for convergence
            if self._abs_compare(prev_x, x) < self.precision:
                break
    
        # Final multiplication to get result
        result = self._standard_multiply(x)
        result.negative = self.negative != other.negative
    
        return result
    
    def _initial_guess_for_division(self, other):
        # Simple initial guess for Newton-Raphson division
        return AdvancedPrecisionNumber('1', self.base, self.precision)

    def _multiply_by_digit(self, digits, n):
        """Multiply a list of digits by a single digit in current base"""
        result = 0
        for d in digits:
            result = result * self.base + d * n
        return result

    
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

    def __pow__(self, n):
        """Calculate power using binary exponentiation in current base"""
        if not isinstance(n, int):
            raise ValueError("Power operation currently supports only integer exponents")
    
        if n == 0:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
    
        if n < 0:
            base_inv = self.inverse()
            return base_inv.__pow__(-n)
    
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        base = AdvancedPrecisionNumber(self)
    
        while n > 0:
            if n & 1:  # If n is odd
                result = result._standard_multiply(base)
            base = base._standard_multiply(base)
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

    # Unary operations
    def sqrt(self):
        """Calculate square root directly in base using digit-by-digit method"""
        try:
            # Input validation
            if self.negative:
                raise ValueError("Cannot calculate square root of negative number")
        
            if self._is_zero():
                return AdvancedPrecisionNumber('0', self.base, self.precision)

            # Precision check
            if self.precision_loss_warning:
                warnings.warn("Result may have reduced precision due to input number")

            # Overflow check for very large numbers
            if len(self.whole_digits) > self.max_precision:
                raise OverflowError("Input number too large for accurate square root calculation")

            # Actual calculation with error tracking
            result = AdvancedPrecisionNumber('0', self.base, self.precision)
            try:
                # Prepare digits for processing
                digits = self.whole_digits + self.fractional_digits
                if len(self.whole_digits) % 2 == 1:
                    digits.insert(0, 0)  # Pad with zero if odd number of digits
    
                # Process pairs of digits
                current = 0
                result_digits = []
    
                for i in range(0, len(digits), 2):
                    # Bring down next pair of digits
                    current = current * (self.base ** 2) + digits[i] * self.base + (digits[i+1] if i+1 < len(digits) else 0)
        
                    # Find next digit of the square root
                    x = 0
                    while (x + 1) * (x + 1) <= current:
                        x += 1
        
                    result_digits.append(x)
                    current -= x * x
    
                # Set whole and fractional parts
                mid_point = (len(self.whole_digits) + 1) // 2
                result.whole_digits = result_digits[:mid_point] or [0]
                result.fractional_digits = (result_digits[mid_point:] + [0] * self.precision)[:self.precision]
    
                return result
            
            except Exception as e:
                raise ValueError(f"Square root calculation failed: {str(e)}")

        except Exception as e:
            raise ValueError(f"Error in square root calculation: {str(e)}")

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
    
        # Convert to integer value
        n = int(self._base_to_decimal())
    
        # Handle special cases
        if n == 0 or n == 1:
            return self._decimal_to_base(1)
    
        # Iterative factorial calculation
        result = 1
        for i in range(2, n + 1):
            result *= i
    
        return self._decimal_to_base(result)

    def log(self, base=None):
        # Result variable is used before initialization
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        try:
            # Input validation
            if self.negative or self._is_zero():
                raise ValueError("Logarithm undefined for non-positive numbers")

            if base is not None:
                if not isinstance(base, (int, float, str, AdvancedPrecisionNumber)):
                    raise TypeError("Base must be a number")
            
                base_num = self._ensure_apn(base)
                if base_num._is_zero() or base_num.negative:
                    raise ValueError("Logarithm base must be positive")
            
                if base_num._abs_compare(AdvancedPrecisionNumber('1', self.base)) == 0:
                    raise ValueError("Logarithm base cannot be 1")

            # Precision checks
            if self.precision_loss_warning:
                warnings.warn("Result may have reduced precision due to input number")

            # Handle special cases
            if self._abs_compare(AdvancedPrecisionNumber('1', self.base)) == 0:
                return AdvancedPrecisionNumber('0', self.base, self.precision)
    
            # Calculate natural logarithm using series expansion
            # ln(x) = 2(a + a³/3 + a⁵/5 + ...) where a = (x-1)/(x+1)
            x = AdvancedPrecisionNumber(self)
            one = AdvancedPrecisionNumber('1', self.base)
    
            # Calculate (x-1)/(x+1)
            a = (x - one)._standard_multiply((x + one).inverse())
    
            # Series expansion
            term = AdvancedPrecisionNumber(a)
            power = AdvancedPrecisionNumber(a)
            divisor = AdvancedPrecisionNumber('1', self.base)
    
            for i in range(1, self.precision * 2, 2):
                result = result + term._standard_multiply(divisor)
                power = power._standard_multiply(a)._standard_multiply(a)
                term = power
                divisor = AdvancedPrecisionNumber(str(i + 2), self.base)
    
            result = result._standard_multiply(AdvancedPrecisionNumber('2', self.base))
    
            # If base is specified, convert to the desired base
            if base is not None:
                base_num = AdvancedPrecisionNumber(str(base), self.base)
                result = result._standard_multiply(base_num.log().inverse())
    
        except Exception as e:
            raise ValueError(f"Error in logarithm calculation: {str(e)}")

    def exp(self):
        """Calculate exponential function using Taylor series in current base"""
        # If number is too large, avoid overflow
        if self._abs_compare(AdvancedPrecisionNumber('100', self.base)) > 0:
            raise ValueError("Argument too large for exponential function")
    
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        term = AdvancedPrecisionNumber('1', self.base)
        x = AdvancedPrecisionNumber(self)
    
        # Taylor series: e^x = 1 + x + x²/2! + x³/3! + ...
        for i in range(1, self.precision * 2):
            term = term._standard_multiply(x)._standard_multiply(
                AdvancedPrecisionNumber(str(1/i), self.base))
            result = result + term
        
            # Check for convergence
            if term._abs_compare(AdvancedPrecisionNumber('1e-' + str(self.precision), self.base)) < 0:
                break
    
        return result

    def inverse(self):
        """Calculate multiplicative inverse (1/x) using Newton's method"""
        if self._is_zero():
            raise ZeroDivisionError("Cannot calculate inverse of zero")
    
        # Initial guess
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        one = AdvancedPrecisionNumber('1', self.base)
    
        for _ in range(self.precision):
            # Newton iteration: x = x * (2 - a*x)
            prev = AdvancedPrecisionNumber(result)
            result = result._standard_multiply(
                AdvancedPrecisionNumber('2', self.base) - 
                self._standard_multiply(result)
            )
        
            # Check for convergence
            if result._abs_compare(prev) == 0:
                break
    
        result.negative = self.negative
        return result

   
    # Trigonometric Functions
    def sin(self):
        if self.precision_loss_warning:
            warnings.warn("Result may have reduced precision")
        
        try:
            # Input validation and normalization
            if not all(isinstance(d, int) for d in self.whole_digits + self.fractional_digits):
                raise ValueError("Invalid digits in number")

            # Range check
            angle = self._normalize_angle()
            if angle._abs_compare(AdvancedPrecisionNumber('1e6', self.base)) > 0:
                warnings.warn("Large angles may result in reduced precision")

            # Precision check
            if self.precision_loss_warning:
                warnings.warn("Result may have reduced precision")

            # Special cases
            if self._is_zero():
                return AdvancedPrecisionNumber('0', self.base, self.precision)

            """Calculate sine using Taylor series in current base"""
            # Normalize angle to [-2π, 2π]
            angle = self._normalize_angle()
    
            result = AdvancedPrecisionNumber('0', self.base, self.precision)
            x = AdvancedPrecisionNumber(angle)
            term = AdvancedPrecisionNumber(x)
    
            # Taylor series: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
            n = 1
            sign = AdvancedPrecisionNumber('1', self.base)
    
            while True:
                result = result + term._standard_multiply(sign)
        
                # Prepare next term
                x_squared = x._standard_multiply(x)
                term = term._standard_multiply(x_squared)
                term = term._standard_multiply(
                    AdvancedPrecisionNumber(str(1/((2*n)*(2*n+1))), self.base)
                )
        
                n += 1
                sign.negative = not sign.negative
        
                # Check for convergence
                if term._abs_compare(
                    AdvancedPrecisionNumber('1e-' + str(self.precision), self.base)) < 0:
                    break
        except Exception as e:
            raise ValueError(f"Error in sine calculation: {str(e)}")
    
        return result

    def cos(self):
        if self.precision_loss_warning:
            warnings.warn("Result may have reduced precision")
        
        """Calculate cosine using Taylor series in current base"""
        # Normalize angle to [-2π, 2π]
        angle = self._normalize_angle()
    
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        x = AdvancedPrecisionNumber(angle)
        term = AdvancedPrecisionNumber('1', self.base)
    
        # Taylor series: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
        n = 1
        sign = AdvancedPrecisionNumber('1', self.base)
        sign.negative = True
    
        x_squared = x._standard_multiply(x)
        term = term._standard_multiply(x_squared)
        term = term._standard_multiply(
            AdvancedPrecisionNumber(str(1/2), self.base)
        )
    
        while True:
            result = result + term._standard_multiply(sign)
        
            # Prepare next term
            term = term._standard_multiply(x_squared)
            term = term._standard_multiply(
                AdvancedPrecisionNumber(str(1/((2*n)*(2*n+1))), self.base)
            )
        
            n += 1
            sign.negative = not sign.negative
        
            # Check for convergence
            if term._abs_compare(
                AdvancedPrecisionNumber('1e-' + str(self.precision), self.base)) < 0:
                break
    
        return result

    def tan(self):
        if self.precision_loss_warning:
            warnings.warn("Result may have reduced precision")
        
        """Calculate tangent using sin/cos ratio"""
        cos_x = self.cos()
        if cos_x._is_zero():
            raise ValueError("Tangent undefined at this point (cos(x) = 0)")
    
        return self.sin()._standard_multiply(cos_x.inverse())

    def arcsin(self):
        if self.precision_loss_warning:
            warnings.warn("Result may have reduced precision")
        
        """Calculate arcsine using Taylor series"""
        if self._abs_compare(AdvancedPrecisionNumber('1', self.base)) > 0:
            raise ValueError("Arcsine argument must be between -1 and 1")
    
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        x = AdvancedPrecisionNumber(self)
        term = AdvancedPrecisionNumber(x)
    
        # Taylor series for arcsin(x)
        n = 0
        coef = AdvancedPrecisionNumber('1', self.base)
        x_squared = x._standard_multiply(x)
    
        while True:
            result = result + term._standard_multiply(coef)
        
            # Calculate next coefficient
            n += 1
            coef = coef._standard_multiply(
                AdvancedPrecisionNumber(str((2*n-1)*(2*n-1)), self.base)
            )._standard_multiply(
                AdvancedPrecisionNumber(str(1/(2*n*(2*n+1))), self.base)
            )
        
            # Prepare next term
            term = term._standard_multiply(x_squared)
        
            # Check for convergence
            if term._abs_compare(
                AdvancedPrecisionNumber('1e-' + str(self.precision), self.base)) < 0:
                break
    
        return result

    def arccos(self):
        if self.precision_loss_warning:
            warnings.warn("Result may have reduced precision")
        
        """Calculate arccosine using arcsin"""
        if self._abs_compare(AdvancedPrecisionNumber('1', self.base)) > 0:
            raise ValueError("Arccosine argument must be between -1 and 1")
    
        # arccos(x) = π/2 - arcsin(x)
        pi_half = self._get_pi()._standard_multiply(
            AdvancedPrecisionNumber('0.5', self.base)
        )
        return pi_half - self.arcsin()

    def arctan(self):
        """Calculate arctangent using Taylor series"""
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
    
        # Use series expansion for |x| <= 1
        # For |x| > 1, use arctan(x) = π/2 - arctan(1/x)
        if self._abs_compare(AdvancedPrecisionNumber('1', self.base)) > 0:
            pi_half = self._get_pi()._standard_multiply(
                AdvancedPrecisionNumber('0.5', self.base)
            )
            return pi_half - self.inverse().arctan()
    
        x = AdvancedPrecisionNumber(self)
        term = AdvancedPrecisionNumber(x)
        x_squared = x._standard_multiply(x)
        sign = AdvancedPrecisionNumber('1', self.base)
    
        # Taylor series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
        n = 1
        while True:
            result = result + term._standard_multiply(sign)
        
            # Prepare next term
            term = term._standard_multiply(x_squared)
            n += 2
            sign.negative = not sign.negative
        
            # Check for convergence
            if term._abs_compare(
                AdvancedPrecisionNumber('1e-' + str(self.precision), self.base)) < 0:
                break
    
        return result

    def _normalize_angle(self):
        """Normalize angle with error handling"""
        try:
            two_pi = self._get_pi()._standard_multiply(
                AdvancedPrecisionNumber('2', self.base)
            )
        
            result = AdvancedPrecisionNumber(self)
            max_iterations = 1000  # Prevent infinite loops
            iteration = 0
        
            while result._abs_compare(two_pi) > 0 and iteration < max_iterations:
                if result.negative:
                    result = result + two_pi
                else:
                    result = result - two_pi
                iteration += 1
            
            if iteration >= max_iterations:
                raise ValueError("Angle normalization failed to converge")
            
            return result
        except Exception as e:
            raise ValueError(f"Error in angle normalization: {str(e)}")

    def _get_pi(self):
        """Calculate π using Chudnovsky algorithm"""
        k = 0
        a_k = AdvancedPrecisionNumber('1', self.base)
        a_sum = AdvancedPrecisionNumber('1', self.base)
        precision_target = self.precision + 10
    
        while k < precision_target:
            k += 1
            a_k = a_k._standard_multiply(
                AdvancedPrecisionNumber(str(-(6*k-5)*(2*k-1)*(6*k-1)), self.base)
            )._standard_multiply(
                AdvancedPrecisionNumber(str(1/(k*k*k*640320*640320)), self.base)
            )
        
            a_sum = a_sum + a_k
        
            if a_k._abs_compare(
                AdvancedPrecisionNumber('1e-' + str(precision_target), self.base)) < 0:
                break
    
        result = AdvancedPrecisionNumber('426880', self.base)._standard_multiply(
            AdvancedPrecisionNumber('10005', self.base).sqrt()
        )._standard_multiply(a_sum.inverse())
    
        return result

            
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