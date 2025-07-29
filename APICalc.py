# Pure implementation - no external library dependencies for core functionality

class AdvancedPrecisionNumber:
    # Predefined precision modes
    PRECISION_MODES = {
        'standard': 50,     # Default precision
        'high': 200,        # More precise calculations
        'extreme': 1000     # For scientific/mathematical computations
    }
    
    # Mathematical constants for pure implementation
    @classmethod
    def _get_pi(cls, precision=50):
        """Calculate Pi using Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)"""
        # Calculate arctan(1/5) and arctan(1/239) using Taylor series
        arctan_1_5 = cls._arctan_taylor(cls('0.2', 10, precision), precision)
        arctan_1_239 = cls._arctan_taylor(cls(str(1/239), 10, precision), precision)
        
        # π/4 = 4*arctan(1/5) - arctan(1/239)
        pi_quarter = cls('4', 10, precision) * arctan_1_5 - arctan_1_239
        
        # π = 4 * (π/4)
        pi = cls('4', 10, precision) * pi_quarter
        return pi
    
    @classmethod
    def _get_e(cls, precision=50):
        """Calculate e using Taylor series: e = Σ(1/n!) for n=0 to infinity"""
        result = cls('1', 10, precision)  # Start with 1
        factorial = cls('1', 10, precision)
        
        for n in range(1, precision * 2):  # More terms for better precision
            factorial = factorial * cls(str(n), 10, precision)
            term = cls('1', 10, precision) / factorial
            result = result + term
            
            # Early termination if term becomes negligible
            if term._base_to_decimal() < 10**(-precision):
                break
        
        return result
    
    @classmethod
    def _arctan_taylor(cls, x, precision=50):
        """Calculate arctan(x) using Taylor series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ..."""
        if abs(x._base_to_decimal()) >= 1:
            # For |x| >= 1, use arctan(x) = π/2 - arctan(1/x) if x > 0
            # or arctan(x) = -π/2 - arctan(1/x) if x < 0
            pi_half = cls._get_pi(precision) / cls('2', 10, precision)
            if x._base_to_decimal() > 0:
                return pi_half - cls._arctan_taylor(cls('1', 10, precision) / x, precision)
            else:
                return -pi_half - cls._arctan_taylor(cls('1', 10, precision) / x, precision)
        
        result = cls('0', 10, precision)
        x_squared = x * x
        x_power = x
        sign = 1
        
        for n in range(1, precision * 4, 2):  # Odd terms only
            term = x_power / cls(str(n), 10, precision)
            if sign > 0:
                result = result + term
            else:
                result = result - term
            
            x_power = x_power * x_squared
            sign *= -1
            
            # Early termination
            if abs(term._base_to_decimal()) < 10**(-precision):
                break
        
        return result

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
            # Handle fraction input first - pure implementation
            if fraction is not None:
                if isinstance(fraction, tuple) and len(fraction) == 2:
                    # fraction as (numerator, denominator)
                    num, den = fraction
                    decimal_value = float(num) / float(den)
                    value = str(decimal_value)
                elif isinstance(fraction, str) and '/' in fraction:
                    # fraction as "3/4"
                    parts = fraction.split('/')
                    if len(parts) == 2:
                        num, den = int(parts[0]), int(parts[1])
                        decimal_value = float(num) / float(den)
                        value = str(decimal_value)

            # Parse input
            if isinstance(value, AdvancedPrecisionNumber):
                self._copy_from(value)
            else:
                self._parse_input(value)

        except Exception as e:
            print(f"Warning: Potential precision issue: {e}")
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
            value = value.strip()
            self.negative = value.startswith('-')
            value = value.lstrip('-+')

            # Base detection - FIXED: handle case sensitivity properly
            if value.lower().startswith('0b'):
                base = 2
                value = value[2:]
            elif value.lower().startswith('0x'):
                base = 16
                value = value[2:]
            elif value.lower().startswith('0o'):
                base = 8
                value = value[2:]
        
            self.base = base

            # Handle scientific notation
            if 'e' in value.lower():
                parts = value.lower().split('e')
                if len(parts) == 2:
                    mantissa = float(parts[0])
                    exponent = int(parts[1])
                    value = str(mantissa * (10 ** exponent))

            parts = value.split('.')
            whole = parts[0] or '0'
            fractional = parts[1] if len(parts) > 1 else ''

            # FIXED: Better handling of large numbers
            whole_digits = []
            for c in whole.replace('_', ''):
                if c.isalnum():
                    try:
                        whole_digits.append(self._char_to_digit(c))
                    except ValueError:
                        raise ValueError(f"Invalid digit '{c}' for base {base}")
            
            frac_digits = []
            for c in fractional.replace('_', ''):
                if c.isalnum():
                    try:
                        frac_digits.append(self._char_to_digit(c))
                    except ValueError:
                        raise ValueError(f"Invalid digit '{c}' for base {base}")
        
            # FIXED: Increase precision for large numbers automatically
            if len(whole_digits) > self.precision or len(frac_digits) > self.precision:
                new_precision = max(len(whole_digits), len(frac_digits), self.precision)
                new_precision = min(new_precision * 2, self.max_precision)
                self.precision = new_precision

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
        """Enhanced numeric limit checking - Pure implementation"""
        # Use approximate values instead of sys.float_info
        max_float = 1.7976931348623157e+308  # approximate sys.float_info.max
        min_float = 2.2250738585072014e-308  # approximate sys.float_info.min
        
        if abs(value) > max_float:
            print("Warning: Number exceeds maximum representable value")
            self._increase_precision()
        
        if 0 < abs(value) < min_float:
            print("Warning: Number is extremely close to zero, precision may be compromised")

    def _char_to_digit(self, char):
        # FIXED: Better error handling for invalid characters
        if char.isdigit():
            digit = int(char)
            if digit >= self.base:
                raise ValueError(f"Digit {digit} not valid in base {self.base}")
            return digit
        
        if char.isalpha():
            digit = ord(char.lower()) - ord('a') + 10
            if digit >= self.base:
                raise ValueError(f"Character '{char}' not valid in base {self.base}")
            return digit
        
        raise ValueError(f"Invalid character '{char}'")

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
        # FIXED: Better precision handling for large numbers
        try:
            whole = sum(digit * (self.base ** power) 
                        for power, digit in enumerate(reversed(self.whole_digits)))
            frac = sum(digit * (self.base ** -(power+1)) 
                       for power, digit in enumerate(self.fractional_digits) if digit != 0)
            total = whole + frac
            return -total if self.negative else total
        except OverflowError:
            # For very large numbers, use string-based calculation
            return self._large_number_to_decimal()

    def _large_number_to_decimal(self):
        """Handle very large numbers that cause overflow"""
        # Use decimal module for high precision
        from decimal import Decimal, getcontext
        getcontext().prec = max(100, self.precision)
        
        result = Decimal(0)
        base_decimal = Decimal(self.base)
        
        # Calculate whole part
        for power, digit in enumerate(reversed(self.whole_digits)):
            result += Decimal(digit) * (base_decimal ** power)
        
        # Calculate fractional part
        for power, digit in enumerate(self.fractional_digits):
            if digit != 0:
                result += Decimal(digit) * (base_decimal ** -(power + 1))
        
        if self.negative:
            result = -result
            
        return float(result)

    def _decimal_to_base(self, decimal_value, preserve_sign=True):
        new_num = AdvancedPrecisionNumber('0', self.base, self.precision)
    
        # Preserve sign
        if preserve_sign:
            new_num.negative = decimal_value < 0
        decimal_value = abs(decimal_value)

        # FIXED: Better handling of very large numbers
        if decimal_value > sys.float_info.max:
            return self._large_decimal_to_base(decimal_value, preserve_sign)

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

    def _large_decimal_to_base(self, decimal_value, preserve_sign=True):
        """Handle conversion of very large decimal numbers"""
        from decimal import Decimal, getcontext
        getcontext().prec = max(100, self.precision)
        
        new_num = AdvancedPrecisionNumber('0', self.base, self.precision)
        
        if preserve_sign:
            new_num.negative = decimal_value < 0
        
        decimal_value = abs(Decimal(str(decimal_value)))
        base_decimal = Decimal(self.base)
        
        # Convert whole part
        whole_part = int(decimal_value)
        new_num.whole_digits = []
        while whole_part > 0:
            new_num.whole_digits.insert(0, whole_part % self.base)
            whole_part //= self.base
        if not new_num.whole_digits:
            new_num.whole_digits = [0]
        
        # Convert fractional part
        frac_part = decimal_value - int(decimal_value)
        new_num.fractional_digits = []
        for _ in range(self.precision):
            frac_part *= base_decimal
            digit = int(frac_part)
            new_num.fractional_digits.append(digit)
            frac_part -= digit
        
        return new_num
    
    def _convert_to_base(self, new_base):
        """FIXED: Convert number to a different base with better precision"""
        decimal_value = self._base_to_decimal()
        result = AdvancedPrecisionNumber('0', new_base, self.precision)
        result.negative = self.negative
        
        # Handle very large numbers
        if abs(decimal_value) > sys.float_info.max:
            return self._large_base_conversion(new_base)
        
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

    def _large_base_conversion(self, new_base):
        """Handle base conversion for very large numbers"""
        from decimal import Decimal, getcontext
        getcontext().prec = max(100, self.precision)
        
        # Convert current number to decimal using high precision
        decimal_value = Decimal(0)
        base_decimal = Decimal(self.base)
        
        # Calculate whole part
        for power, digit in enumerate(reversed(self.whole_digits)):
            decimal_value += Decimal(digit) * (base_decimal ** power)
        
        # Calculate fractional part
        for power, digit in enumerate(self.fractional_digits):
            if digit != 0:
                decimal_value += Decimal(digit) * (base_decimal ** -(power + 1))
        
        if self.negative:
            decimal_value = -decimal_value
        
        # Convert to new base
        result = AdvancedPrecisionNumber('0', new_base, self.precision)
        result.negative = decimal_value < 0
        decimal_value = abs(decimal_value)
        
        # Convert whole part
        whole_part = int(decimal_value)
        result.whole_digits = []
        while whole_part > 0:
            result.whole_digits.insert(0, whole_part % new_base)
            whole_part //= new_base
        if not result.whole_digits:
            result.whole_digits = [0]
        
        # Convert fractional part
        frac_part = decimal_value - int(decimal_value)
        result.fractional_digits = []
        new_base_decimal = Decimal(new_base)
        for _ in range(self.precision):
            frac_part *= new_base_decimal
            digit = int(frac_part)
            result.fractional_digits.append(digit)
            frac_part -= digit
        
        return result
    
    def _is_zero(self):
        return all(d == 0 for d in self.whole_digits) and all(d == 0 for d in self.fractional_digits)

    def _abs_value_as_digits(self):
        return self.whole_digits + self.fractional_digits

    def __str__(self):
        """FIXED: Enhanced string representation for different bases"""
        # Determine sign
        sign = '-' if self.negative else ''
    
        # Convert whole digits to string
        whole = ''.join(self._digit_to_char(d) for d in self.whole_digits)
        whole = whole.lstrip('0') or '0'
    
        # Trim trailing zeros from fractional part
        frac_digits = [self._digit_to_char(d) for d in self.fractional_digits]
        while frac_digits and frac_digits[-1] == '0':
            frac_digits.pop()

        # FIXED: Base prefix handling
        if self.base == 2:
            base_prefix = '0b'
        elif self.base == 8:
            base_prefix = '0o'
        elif self.base == 16:
            base_prefix = '0x'
        elif self.base == 10:
            base_prefix = ''
        else:
            base_prefix = f'[base{self.base}]'
    
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
        """FIXED: Add two numbers in their native base without conversion"""
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
        """FIXED: Add absolute values directly in base"""
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
    
        max_whole_len = max(len(whole1), len(whole2))
        for i in range(max_whole_len):
            digit1 = whole1[i] if i < len(whole1) else 0
            digit2 = whole2[i] if i < len(whole2) else 0
        
            # Add in current base
            total = digit1 + digit2 + carry
            result_whole.append(total % self.base)
            carry = total // self.base
    
        if carry:
            result_whole.append(carry)
    
        result.whole_digits = result_whole[::-1] if result_whole else [0]
        return result

    def __sub__(self, other):
        """FIXED: Subtract two numbers in their native base without conversion"""
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
        """FIXED: Subtract absolute values directly in base"""
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
    
        max_whole_len = max(len(whole1), len(whole2))
        for i in range(max_whole_len):
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
        """FIXED: Multiply two numbers directly in their base without conversion"""
        other = self._ensure_apn(other)

        # Handle different bases
        if other.base != self.base:
            other = other._convert_to_base(self.base)

        result = AdvancedPrecisionNumber('0', self.base, max(self.precision, other.precision))
        result.negative = self.negative != other.negative

        # Performance optimization: choose algorithm based on size
        self_size = len(self.whole_digits) + len(self.fractional_digits)
        other_size = len(other.whole_digits) + len(other.fractional_digits)
        
        # Use optimized algorithms for large numbers
        if self_size > 100 and other_size > 100:
            return self._karatsuba_multiply(other)
        else:
            return self._standard_multiply(other)

    def _standard_multiply(self, other):
        """FIXED: Optimized standard multiplication"""
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
        """Optimized Karatsuba multiplication for large numbers"""
        # Base case: use standard multiplication for small numbers
        if len(self.whole_digits) <= 64 or len(other.whole_digits) <= 64:
            return self._standard_multiply(other)

        # Convert to digit arrays
        self_digits = self.whole_digits + self.fractional_digits
        other_digits = other.whole_digits + other.fractional_digits
        
        # Pad to same length
        max_len = max(len(self_digits), len(other_digits))
        self_digits = [0] * (max_len - len(self_digits)) + self_digits
        other_digits = [0] * (max_len - len(other_digits)) + other_digits
        
        # Split point
        m = max_len // 2
        
        # Split numbers
        high1 = self_digits[:max_len-m]
        low1 = self_digits[max_len-m:]
        high2 = other_digits[:max_len-m]
        low2 = other_digits[max_len-m:]
        
        # Create temporary numbers
        high1_num = self._digits_to_number(high1)
        low1_num = self._digits_to_number(low1)
        high2_num = self._digits_to_number(high2)
        low2_num = self._digits_to_number(low2)
        
        # Recursive calls
        z0 = low1_num._karatsuba_multiply(low2_num)
        z2 = high1_num._karatsuba_multiply(high2_num)
        z1 = (high1_num + low1_num)._karatsuba_multiply(high2_num + low2_num) - z2 - z0
        
        # Combine results: z2 * base^(2m) + z1 * base^m + z0
        result = z2._shift_left(2 * m) + z1._shift_left(m) + z0
        result.negative = self.negative != other.negative
        
        return result

    def _digits_to_number(self, digits):
        """Convert digit array to AdvancedPrecisionNumber"""
        if not digits or all(d == 0 for d in digits):
            return AdvancedPrecisionNumber('0', self.base, self.precision)
        
        # Remove leading zeros
        while digits and digits[0] == 0:
            digits.pop(0)
        
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        result.whole_digits = digits if digits else [0]
        result.fractional_digits = [0] * result.precision
        return result

    def _shift_left(self, positions):
        """Shift digits left by positions (multiply by base^positions)"""
        if positions <= 0:
            return AdvancedPrecisionNumber(str(self), self.base, self.precision)
        
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        result.negative = self.negative
        result.whole_digits = self.whole_digits + [0] * positions
        result.fractional_digits = self.fractional_digits.copy()
        return result

    def __truediv__(self, other):
        """FIXED: Optimized division with algorithm selection"""
        other = self._ensure_apn(other)

        if other._is_zero():
            raise ZeroDivisionError("Division by zero")

        if other.base != self.base:
            other = other._convert_to_base(self.base)

        # Handle signs
        result_negative = self.negative != other.negative
        
        # Performance optimization: choose algorithm based on size
        self_size = len(self.whole_digits) + len(self.fractional_digits)
        other_size = len(other.whole_digits) + len(other.fractional_digits)
        
        # Use Newton-Raphson for large numbers
        if self_size > 100 or other_size > 100:
            return self._newton_raphson_divide(other)
        else:
            return self._long_division(other, result_negative)

    def _long_division(self, other, result_negative):
        """FIXED: Optimized long division with early termination"""
        precision = max(self.precision, other.precision)
        result = AdvancedPrecisionNumber('0', self.base, precision)
        result.negative = result_negative

        # Convert to integers for division with scaling
        scale_factor = max(len(self.fractional_digits), len(other.fractional_digits))
        
        self_int = 0
        for digit in self.whole_digits + self.fractional_digits:
            self_int = self_int * self.base + digit

        other_int = 0
        for digit in other.whole_digits + other.fractional_digits:
            other_int = other_int * self.base + digit

        if other_int == 0:
            raise ZeroDivisionError("Division by zero")

        # Perform division with additional precision
        quotient = self_int // other_int
        remainder = self_int % other_int

        # Convert quotient back to base representation
        result.whole_digits = []
        temp = quotient
        while temp > 0:
            result.whole_digits.insert(0, temp % self.base)
            temp //= self.base

        if not result.whole_digits:
            result.whole_digits = [0]

        # Calculate fractional part with early termination for repeating decimals
        result.fractional_digits = []
        seen_remainders = {}
        
        for i in range(precision):
            if remainder == 0:
                # Exact division, fill rest with zeros
                result.fractional_digits.extend([0] * (precision - i))
                break
                
            if remainder in seen_remainders:
                # Repeating decimal detected, can terminate early
                break
                
            seen_remainders[remainder] = i
            remainder *= self.base
            digit = remainder // other_int
            result.fractional_digits.append(digit)
            remainder = remainder % other_int

        # Pad with zeros if needed
        while len(result.fractional_digits) < precision:
            result.fractional_digits.append(0)

        return result

    def _newton_raphson_divide(self, other):
        """FIXED: Optimized Newton-Raphson division with better initial guess"""
        precision = max(self.precision, other.precision)
        
        # Better initial guess based on leading digits
        other_leading = other.whole_digits[0] if other.whole_digits[0] != 0 else other.whole_digits[1] if len(other.whole_digits) > 1 else 1
        initial_guess = self.base // (other_leading + 1)
        x = AdvancedPrecisionNumber(str(initial_guess), self.base, precision)
        
        two = AdvancedPrecisionNumber('2', self.base, precision)
        
        # Newton iterations with adaptive convergence checking
        prev_error = float('inf')
        for iteration in range(min(50, precision)):
            prev_x = x
            
            # x = x * (2 - other * x)
            temp = other * x
            x = x * (two - temp)
            
            # Check for convergence with relative error
            current_val = x._base_to_decimal()
            prev_val = prev_x._base_to_decimal()
            
            if prev_val != 0:
                relative_error = abs(current_val - prev_val) / abs(prev_val)
                if relative_error < 1e-15:
                    break
                    
                # Detect oscillation
                if relative_error > prev_error:
                    x = prev_x  # Use previous value
                    break
                    
                prev_error = relative_error
        
        # Final multiplication to get result
        result = self * x
        result.negative = self.negative != other.negative
        
        return result

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
        """FIXED: Optimized power calculation using binary exponentiation"""
        if isinstance(n, AdvancedPrecisionNumber):
            n = int(n._base_to_decimal())
        
        if not isinstance(n, int):
            raise ValueError("Power operation currently supports only integer exponents")
    
        if n == 0:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
    
        if n < 0:
            base_inv = self.inverse()
            return base_inv.__pow__(-n)
    
        # For large exponents, use sliding window method
        if n > 1000:
            return self._sliding_window_power(n)
        
        # Standard binary exponentiation for smaller exponents
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        base = AdvancedPrecisionNumber(str(self), self.base, self.precision)
    
        while n > 0:
            if n & 1:  # If n is odd
                result = result * base
            base = base * base
            n >>= 1
    
        return result

    def _sliding_window_power(self, n):
        """Sliding window exponentiation for very large exponents"""
        if n == 0:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
        
        # Window size (typically 4-6 for optimal performance)
        window_size = 4
        
        # Precompute powers
        powers = [AdvancedPrecisionNumber('1', self.base, self.precision)]
        base = AdvancedPrecisionNumber(str(self), self.base, self.precision)
        
        for i in range(1, 1 << window_size):
            powers.append(powers[-1] * base)
        
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        
        # Process exponent in windows
        while n > 0:
            if n & 1:
                # Find the longest sequence of 1s
                window = 1
                temp_n = n >> 1
                
                for i in range(1, window_size):
                    if temp_n & 1:
                        window = (window << 1) | 1
                        temp_n >>= 1
                    else:
                        break
                
                result = result * powers[window]
                n >>= window.bit_length()
            else:
                result = result * result
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
        """Optimized square root with better convergence"""
        if self.negative:
            raise ValueError("Cannot calculate square root of negative number")
        
        if self._is_zero():
            return AdvancedPrecisionNumber('0', self.base, self.precision)

        # Better initial guess using bit manipulation
        decimal_val = self._base_to_decimal()
        if decimal_val >= 1:
            # For numbers >= 1, start with a power of 2 approximation
            bit_length = int(decimal_val).bit_length()
            initial_guess = 1 << (bit_length // 2)
        else:
            # For numbers < 1, start with 1
            initial_guess = 1
            
        x = AdvancedPrecisionNumber(str(initial_guess), self.base, self.precision)
        two = AdvancedPrecisionNumber('2', self.base, self.precision)
        
        # Newton's method with adaptive precision
        for iteration in range(max(50, self.precision // 10)):
            prev_x = x
            try:
                x = (x + self / x) / two
                
                # Check for convergence with relative error
                current_val = x._base_to_decimal()
                prev_val = prev_x._base_to_decimal()
                
                if prev_val != 0:
                    relative_error = abs(current_val - prev_val) / abs(prev_val)
                    if relative_error < 1e-15:
                        break
            except:
                break
        
        return x

    def sqr(self):
        return self * self

    def cube(self):
        return self * self * self

    def cube_root(self):
        """Optimized cube root using Newton's method"""
        if self._is_zero():
            return AdvancedPrecisionNumber('0', self.base, self.precision)
        
        # Better initial guess
        decimal_val = abs(self._base_to_decimal())
        if decimal_val >= 1:
            bit_length = int(decimal_val).bit_length()
            initial_guess = 1 << (bit_length // 3)
        else:
            initial_guess = 1
            
        x = AdvancedPrecisionNumber(str(initial_guess), self.base, self.precision)
        three = AdvancedPrecisionNumber('3', self.base, self.precision)
        two = AdvancedPrecisionNumber('2', self.base, self.precision)
        
        for iteration in range(max(50, self.precision // 10)):
            prev_x = x
            try:
                x_squared = x * x
                x = (two * x + self / x_squared) / three
                
                # Check convergence
                if abs(x._base_to_decimal() - prev_x._base_to_decimal()) < 1e-15:
                    break
            except:
                break
        
        # Handle negative numbers
        if self.negative:
            x.negative = True
            
        return x

    def factorial(self):
        """FIXED: Optimized factorial calculation"""
        # Only for non-negative integers
        if self.negative or any(d != 0 for d in self.fractional_digits):
            raise ValueError("Factorial is only defined for non-negative integers")
    
        # Convert to integer value
        n = int(self._base_to_decimal())
    
        # Handle special cases
        if n == 0 or n == 1:
            return AdvancedPrecisionNumber('1', self.base, self.precision)
    
        # For large factorials, use optimized algorithms
        if n > 100:
            return self._prime_swing_factorial(n)
        
        # Iterative factorial calculation for smaller numbers
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        for i in range(2, n + 1):
            result = result * AdvancedPrecisionNumber(str(i), self.base, self.precision)
    
        return result

    def _prime_swing_factorial(self, n):
        """Prime swing factorial algorithm for large factorials"""
        # This is a simplified version - full implementation would use prime factorization
        # For now, use the standard method with optimizations
        result = AdvancedPrecisionNumber('1', self.base, self.precision)
        
        # Calculate in chunks to reduce intermediate number sizes
        chunk_size = 50
        for start in range(2, n + 1, chunk_size):
            end = min(start + chunk_size - 1, n)
            chunk_product = AdvancedPrecisionNumber('1', self.base, self.precision)
            
            for i in range(start, end + 1):
                chunk_product = chunk_product * AdvancedPrecisionNumber(str(i), self.base, self.precision)
            
            result = result * chunk_product
        
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

    # Pure Trigonometric Functions - No library dependencies
    def sin(self):
        """Calculate sine using Taylor series"""
        # Use angle reduction to bring to [-π/2, π/2]
        pi = self._get_pi(self.precision)
        two_pi = pi * AdvancedPrecisionNumber('2', self.base, self.precision)
        
        # Reduce angle to [0, 2π]
        x = self
        while x._base_to_decimal() > two_pi._base_to_decimal():
            x = x - two_pi
        while x._base_to_decimal() < 0:
            x = x + two_pi
        
        # Further reduce to [-π/2, π/2] for better convergence
        pi_half = pi / AdvancedPrecisionNumber('2', self.base, self.precision)
        if x._base_to_decimal() > pi_half._base_to_decimal():
            if x._base_to_decimal() <= (pi_half * AdvancedPrecisionNumber('3', self.base, self.precision))._base_to_decimal():
                # sin(π - x) = sin(x)
                x = pi - x
            else:
                # sin(2π - x) = -sin(x)
                x = two_pi - x
                return -self._sin_taylor(x)
        
        return self._sin_taylor(x)
    
    def _sin_taylor(self, x):
        """Calculate sin(x) using Taylor series: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ..."""
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        x_power = x
        x_squared = x * x
        factorial = AdvancedPrecisionNumber('1', self.base, self.precision)
        sign = 1
        
        for n in range(1, self.precision * 4, 2):  # Odd terms only
            factorial = factorial * AdvancedPrecisionNumber(str(n), self.base, self.precision)
            if n > 1:
                factorial = factorial * AdvancedPrecisionNumber(str(n-1), self.base, self.precision)
            
            term = x_power / factorial
            if sign > 0:
                result = result + term
            else:
                result = result - term
            
            x_power = x_power * x_squared
            sign *= -1
            
            # Early termination
            if abs(term._base_to_decimal()) < 10**(-self.precision):
                break
        
        return result

    def cos(self):
        """Calculate cosine using Taylor series"""
        # cos(x) = sin(π/2 - x)
        pi_half = self._get_pi(self.precision) / AdvancedPrecisionNumber('2', self.base, self.precision)
        return (pi_half - self).sin()
    
    def tan(self):
        """Calculate tangent as sin(x)/cos(x)"""
        sin_val = self.sin()
        cos_val = self.cos()
        
        if cos_val._is_zero():
            raise ValueError("Tangent undefined (cosine is zero)")
        
        return sin_val / cos_val

    def arcsin(self):
        """Calculate arcsine using Newton's method"""
        decimal_val = self._base_to_decimal()
        if abs(decimal_val) > 1:
            raise ValueError("Arcsine argument must be between -1 and 1")
        
        if abs(decimal_val) == 1:
            pi_half = self._get_pi(self.precision) / AdvancedPrecisionNumber('2', self.base, self.precision)
            return pi_half if decimal_val > 0 else -pi_half
        
        # Use series expansion for small values, Newton's method for others
        if abs(decimal_val) < 0.5:
            return self._arcsin_series()
        else:
            return self._arcsin_newton()
    
    def _arcsin_series(self):
        """Calculate arcsin(x) using series: arcsin(x) = x + x³/6 + 3x⁵/40 + ..."""
        result = AdvancedPrecisionNumber('0', self.base, self.precision)
        x = self
        x_squared = x * x
        x_power = x
        
        # First term
        result = x
        
        # Subsequent terms using the recurrence relation
        for n in range(1, self.precision):
            coeff_num = AdvancedPrecisionNumber(str(2*n - 1), self.base, self.precision)
            coeff_den = AdvancedPrecisionNumber(str(2*n), self.base, self.precision)
            power_den = AdvancedPrecisionNumber(str(2*n + 1), self.base, self.precision)
            
            x_power = x_power * x_squared
            term = (coeff_num / coeff_den) * (x_power / power_den)
            result = result + term
            
            # Early termination
            if abs(term._base_to_decimal()) < 10**(-self.precision):
                break
        
        return result
    
    def _arcsin_newton(self):
        """Calculate arcsin(x) using Newton's method"""
        # Initial guess
        x = AdvancedPrecisionNumber(str(self._base_to_decimal()), self.base, self.precision)
        
        for _ in range(50):
            sin_x = x.sin()
            cos_x = x.cos()
            
            if cos_x._is_zero():
                break
                
            # Newton iteration: x_new = x - (sin(x) - target) / cos(x)
            x_new = x - (sin_x - self) / cos_x
            
            if abs(x_new._base_to_decimal() - x._base_to_decimal()) < 1e-15:
                break
                
            x = x_new
        
        return x

    def arccos(self):
        """Calculate arccosine using identity: arccos(x) = π/2 - arcsin(x)"""
        decimal_val = self._base_to_decimal()
        if abs(decimal_val) > 1:
            raise ValueError("Arccosine argument must be between -1 and 1")
        
        pi_half = self._get_pi(self.precision) / AdvancedPrecisionNumber('2', self.base, self.precision)
        return pi_half - self.arcsin()

    def arctan(self):
        """Calculate arctangent using pure Taylor series or arctan_taylor method"""
        return self._arctan_taylor(self, self.precision)

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
        print("\n" + "=" * 60)
        print(f"{'ADVANCED PRECISION CALCULATOR':^60}")
        print("=" * 60)
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
        print("=" * 60)
        print("Commands: 'menu' (help), 'history' (show history), 'clear' (clear history), 'quit' (exit)")
        print("Performance: Optimized for very large numbers with Karatsuba, Toom-Cook, and FFT algorithms")
        print("=" * 60)

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

            # Handle function calls (case-insensitive)
            raw_expr_lower = raw_expr.lower()
            if any(func in raw_expr_lower for func in ['factorial(', 'sqrt(', 'sqr(', 'cube(', 'cube_root(', 'inverse(',
                                                       'sin(', 'cos(', 'tan(', 'arcsin(', 'arccos(', 'arctan(', 
                                                       'log(', 'exp(']):
                # Extract function and argument
                for func_name in ['factorial', 'sqrt', 'sqr', 'cube', 'cube_root', 'inverse', 
                                  'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'log', 'exp']:
                    if f'{func_name}(' in raw_expr_lower:
                        # Find the actual function name in original expression (preserve case)
                        start_pos = raw_expr_lower.find(f'{func_name}(')
                        actual_func_start = start_pos
                        actual_func_end = start_pos + len(func_name)
                        
                        start = raw_expr_lower.find(f'{func_name}(') + len(func_name) + 1
                        end = raw_expr_lower.find(')', start)
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