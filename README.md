# Advanced Precision Calculator

## Problem Statement

Write an arbitrary-precision calculator in a language that doesn't have native support and without relying on any libraries for the core functionality. Wrap it in a REPL. It should support at least addition, subtraction, multiplication, division (and modulo), exponentiation and factorial. Bonus points for supporting non-decimal bases, fractions, logarithms, etc.

## Overview

A comprehensive arbitrary-precision calculator implemented in Python without relying on external libraries for core mathematical operations. This calculator supports multiple number bases, complex numbers, matrix operations, advanced mathematical functions, and provides multiple interfaces including REPL, modern web interface, and API endpoints.

🎉 **NEW FEATURES:**
- ✅ **Matrix Operations**: Full matrix arithmetic with arbitrary precision elements
- ✅ **Complex Number Support**: Full complex arithmetic (3+4i, 2-5j, etc.)
- ✅ **Web Interface**: Beautiful, responsive web calculator
- ✅ **Enhanced REPL**: Interactive command-line interface with history
- ✅ **REST API**: Flask-based web server with JSON endpoints
- ✅ **Pure Implementation**: All mathematical functions without external libraries

The project includes:
- **Python Core Engine**: Full-featured arbitrary precision calculator with complex number support
- **Web Interface**: Modern Flask-based web application with interactive UI
- **REPL Interface**: Enhanced command-line interface with history and advanced features
- **REST API Server**: JSON-based API for web integration
- **Multiple Frontends**: Both web interface and React-based calculator
- **Complete Integration**: Works offline, online, and as API service

Here's what the new web interface looks like:
![Advanced Precision Calculator Web Interface](screenshots/web-calculator.png)
🌐 **Web Calculator**: Available at `http://localhost:5000` when running locally
🌐 **Live Demo**: https://apicalculator-v1.netlify.app/

## Architecture

### Backend (Python)
- **Core Engine**: `APICalc.py` - Pure Python implementation with arbitrary precision and complex numbers
- **Web Server**: `app.py` - Flask-based web application with REST API endpoints
- **REPL Interface**: Enhanced command-line interface with history and advanced features
- **API Server**: `api_server.py` - Alternative Flask-based REST API (optional)
- **Test Suite**: Multiple test files for comprehensive validation

### Frontend (React + TypeScript)
- **Modern Web Interface**: Built with React, TypeScript, and Tailwind CSS
- **Calculator Page**: Interactive calculator with visual button interface
- **Test Interface**: Web-based test runner for validation
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Dual Calculator**: JavaScript implementation for offline use + API integration

### Deployment Options
1. **Static Site** (Netlify): Uses embedded JavaScript calculator
2. **Full Stack** (Local): Python API + React frontend
3. **Hybrid**: Python CLI + JavaScript web interface

## Features

### Core Arithmetic Operations
- **Addition** (`+`): Add two numbers (real or complex)
- **Subtraction** (`-`): Subtract two numbers (real or complex)
- **Multiplication** (`*`): Multiply two numbers (real or complex)
- **Division** (`/`): Divide two numbers with arbitrary precision (real or complex)
- **Floor Division** (`//`): Integer division
- **Modulo** (`%`): Remainder operation
- **Exponentiation** (`**`): Raise to power (supports complex bases and exponents)

### Advanced Mathematical Functions
- **Factorial** (`factorial(n)` or `n!`): Calculate factorial without libraries
- **Square Root** (`sqrt(n)`): Calculate square root (real and complex)
- **Square** (`sqr(n)`): Calculate square (n²)
- **Cube** (`cube(n)`): Calculate cube (n³)
- **Cube Root** (`cube_root(n)`): Calculate cube root
- **Logarithm** (`log(n)` or `log(n, base)`): Natural or base logarithm (pure, supports complex)
- **Exponential** (`exp(n)`): Calculate e^n (pure, supports complex)
- **Inverse** (`inverse(n)`): Calculate 1/n

### Trigonometric Functions
- **Sine** (`sin(x)`): Calculate sine (pure, supports complex numbers)
- **Cosine** (`cos(x)`): Calculate cosine (pure, supports complex numbers)
- **Tangent** (`tan(x)`): Calculate tangent (pure, supports complex numbers)
- **Arcsine** (`arcsin(x)`): Calculate inverse sine (pure)
- **Arccosine** (`arccos(x)`): Calculate inverse cosine (pure)
- **Arctangent** (`arctan(x)`): Calculate inverse tangent (pure)

### Number Base Support
- **Binary** (`0b1010`): Base-2 numbers
- **Octal** (`0o17`): Base-8 numbers
- **Decimal** (default): Base-10 numbers
- **Hexadecimal** (`0xFF`): Base-16 numbers
- **Custom Bases**: Support for bases 2-36

### Complex Number Support
- **Complex Creation**: Create complex numbers (3+4i, 2-5j, 7i, -3i)
- **Complex Arithmetic**: All basic operations work with complex numbers
- **Complex Functions**: Trigonometric, exponential, and logarithmic functions
- **Magnitude** (`abs(z)`): Calculate |z| = √(a² + b²)
- **Conjugate** (`conjugate(z)`): Calculate z* = a - bi
- **Argument** (`arg(z)`): Calculate phase angle of complex number
- **Polar Form**: Create complex numbers from magnitude and phase

### Fraction Support
- **Fraction Conversion** (`to_fraction()`): Convert to fraction representation
- **Fraction Input**: Initialize with fraction values
- **Fraction Arithmetic**: Perform operations on fractions

### Matrix Operations
- **Matrix Creation**: Create matrices from lists or using utility functions
- **Matrix Arithmetic**: Addition, subtraction, multiplication with arbitrary precision
- **Matrix Transpose** (`transpose(m)`): Calculate matrix transpose
- **Matrix Determinant** (`determinant(m)`): Calculate determinant for square matrices
- **Matrix Inverse** (`inverse(m)`): Calculate matrix inverse (when it exists)
- **Matrix Trace** (`trace(m)`): Calculate trace (sum of diagonal elements)
- **Special Matrices**: Identity (`identity(n)`), zeros (`zeros(r, c)`), ones (`ones(r, c)`)
- **Complex Matrix Support**: All operations work with complex number matrices
- **Arbitrary Precision**: All matrix elements maintain full arbitrary precision

## Usage

### 🌐 Web Interface (Recommended)

**Option 1: Local Web Interface**
```bash
python demo_calculator.py
# Opens web browser automatically to http://localhost:5000
```

**Option 2: Online Demo**
Visit **https://apicalculator-v1.netlify.app/** to use the React-based calculator immediately - no installation required!

### 💻 Local Development

#### Option 1: Frontend Only (Static)

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Navigate to the application:**
   - **Home Page**: Overview and navigation
   - **Calculator**: Interactive calculator interface
   - **Tests**: Web-based test runner

#### Option 2: Full Stack (API + Frontend)

1. **Start both servers simultaneously:**
   ```bash
   # Windows
   .\start_local.bat
   
   # Or manually:
   # Terminal 1: python api_server.py
   # Terminal 2: npm run dev
   ```

#### Option 3: Python CLI Only

```bash
python APICalc.py
```

**Enhanced REPL Commands:**
- `menu` - Show comprehensive help menu with all available operations
- `history` - Display calculation history (last 10 calculations)
- `clear` - Clear calculation history
- `quit` or `exit` - Exit the calculator

**Complex Number Support in REPL:**
- Type complex numbers directly: `3+4i`, `2-5j`, `7i`, `-3i`
- Use complex functions: `abs(3+4i)`, `conjugate(2-3i)`, `arg(1+i)`
- Complex arithmetic: `(3+4i) * (1-2i)`, `(2+3i) ** 2`

**Matrix Operations in REPL:**
- Create matrices: `matrix([[1,2],[3,4]])` or use matrix literals `[[1,2],[3,4]]`
- Matrix functions: `identity(3)`, `zeros(2,3)`, `ones(3,2)`
- Matrix operations: `transpose(m)`, `determinant(m)`, `trace(m)`, `inverse(m)`
- Complex matrices: `[["1+2i", "3-i"], ["4i", "2"]]`
- All operations support arbitrary precision elements

### Example Usage

#### Web Interface
- **Modern UI**: Beautiful, responsive interface that works on desktop and mobile
- **Button Grid**: Visual calculator buttons for easy input
- **Direct Input**: Type expressions directly in the input field
- **Complex Numbers**: Full support for complex number input and operations
- **Mathematical Functions**: Access to all trigonometric, logarithmic, and advanced functions
- **Settings Panel**: Configure precision (Standard/High/Extreme), number base, and display mode
- **History System**: Persistent calculation history with click-to-reuse functionality
- **Advanced Panel**: Quick access to specialized functions and complex number examples
- **Error Handling**: User-friendly error messages and validation
- **Keyboard Shortcuts**: Full keyboard navigation support

Here's how the new web calculator interface looks:
![Advanced Precision Calculator Web Interface](screenshots/web-calculator.png)
![API Calculator.](screenshots/calc.png)
![API Calculator.](screenshots/calc2.png)

#### Command Line
```
>>> 123 + 456
579

>>> factorial(5)
120

>>> sqrt(16)
4.0

>>> 0b1010 + 0x10
0b11010

>>> sin(3.14159/2)
0.9999999999999999

>>> log(100, 10)
2.0

>>> to_fraction(0.75)
3/4

# Complex Number Examples
>>> 3+4i
3+4i

>>> abs(3+4i)
5

>>> (3+4i) * (1-2i)
11-2i

>>> sin(1+2i)
3.165778513216168+1.959601041421606i

>>> conjugate(3-4i)
3+4i

# Matrix Examples
>>> identity(3)
[
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1]
]

>>> zeros(2, 3)
[
  [0, 0, 0],
  [0, 0, 0]
]

>>> transpose([[1, 2, 3], [4, 5, 6]])
[
  [1, 4],
  [2, 5],
  [3, 6]
]

>>> determinant([[1, 2], [3, 4]])
-2
```

### Advanced Examples

```
>>> 2 ** 100
1267650600228229401496703205376

>>> factorial(20)
2432902008176640000

>>> 0xFF * 0b1010
0xa0a

>>> sqrt(2) ** 2
2.0000000000000004

# Complex Number Advanced Examples
>>> sqrt(-1)
1i

>>> (3+4i) ** 2
-7+24i

>>> exp(1+2i)
-1.1312043837568135+2.4717266720048188i

>>> log(1+i)
0.34657359027997264+0.7853981633974483i

# Advanced Matrix Examples
>>> m1 = [[1, 2], [3, 4]]
>>> m2 = [[5, 6], [7, 8]]
>>> matrix_add(m1, m2)
[
  [6, 8],
  [10, 12]
]

>>> matrix_multiply(m1, m2)
[
  [19, 22],
  [43, 50]
]

>>> trace([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
15

# Complex Matrix Example
>>> complex_matrix = [["1+2i", "3-i"], ["0+4i", "2"]]
>>> transpose(complex_matrix)
[
  [1+2i, 4i],
  [3-1i, 2]
]
```

## Implementation Details

### Calculator Implementations

#### Python Core (`APICalc.py`)
- **Precision Modes**: Standard (50 digits), High (200 digits), Extreme (1000 digits)
- **Complex Numbers**: Full support for complex arithmetic and functions
- **Matrix Operations**: Complete matrix arithmetic with arbitrary precision elements
- **Algorithms**: Karatsuba multiplication, Newton-Raphson division, binary exponentiation
- **Features**: Full arbitrary precision, all mathematical functions, pure implementation
- **Mathematical Constants**: Pi and e calculated using pure iterative methods

#### JavaScript Frontend (`src/utils/calculator.ts`)
- **Precision**: JavaScript number precision (sufficient for most use cases)
- **Features**: Basic arithmetic, factorial, square root, base conversion
- **Benefits**: Offline operation, instant response, no server required

### Integration Architecture

#### Web Interface Deployment (Flask)
- Python Flask server with HTML/CSS/JavaScript frontend
- Full arbitrary precision support including complex numbers
- REST API endpoints for programmatic access
- Real-time calculations with user-friendly interface
- Supports all advanced mathematical functions
- History management and settings persistence

#### Static Deployment (Netlify)
- Uses JavaScript calculator for all operations
- No backend server required
- Works offline after initial load
- Instant calculations
- Limited to JavaScript number precision

#### Full Stack Deployment
- Python API server provides full arbitrary precision
- React frontend calls API endpoints
- Supports all advanced mathematical functions
- Requires server infrastructure

### Error Handling
- Division by zero protection
- Invalid input validation for complex numbers
- Precision loss warnings (Python only)
- Domain validation for mathematical functions (real and complex)
- Complex number parsing validation
- TypeScript type safety (Frontend)
- User-friendly error modals in web interface
- API error responses with detailed messages

## Testing

## Testing

### 🌐 Web Interface Tests
Access the test interface at https://apicalculator-v1.netlify.app/test or locally at `/test` to run comprehensive test suites with visual feedback.

**Current Test Categories:**
- **Basic Arithmetic** (4 tests): Addition, subtraction, multiplication, division
- **Large Numbers** (2 tests): Operations with very large integers
- **Advanced Functions** (4 tests): Factorial, square root, power operations
- **Base Conversions** (2 tests): Binary and hexadecimal arithmetic
- **Error Handling** (2 tests): Division by zero, invalid expressions

**Features:**
- ✅ **Interactive Test Runner**: Run individual tests or full test suites
- ✅ **Real-time Results**: See test progress and results as they execute
- ✅ **Category Filtering**: Filter tests by mathematical operation type
- ✅ **Visual Feedback**: Green/red indicators for pass/fail status
- ✅ **Detailed Output**: See expected vs actual results for each test
- ✅ **Performance Metrics**: Execution time for each test case
- ✅ **JavaScript Calculator Testing**: Uses the local TypeScript implementation

### 🐍 Python Tests
```bash
python test_APICalc.py
```

**Test Suite Coverage (14 tests - ✅ 100% passing):**
- **Initialization Tests**: Basic number creation and parsing
- **Arithmetic Operations**: Addition, subtraction, multiplication, division
- **Base Conversion**: Binary (0b), hexadecimal (0x), octal (0o) support
- **Advanced Functions**: Factorial, square root, power operations, modulo
- **Trigonometric Functions**: Sine, cosine with built-in math library
- **Logarithmic Functions**: Natural logarithm calculations
- **Fraction Support**: Conversion to Python fractions
- **Comparison Operations**: All comparison operators (>, <, ==, !=, etc.)
- **Error Handling**: Division by zero, negative square roots, invalid factorials
- **Data Types**: String representation, hash functionality, object methods

**Advanced Test Features:**
- ✅ **Custom Test Runner**: Enhanced reporting with detailed pass/fail statistics
- ✅ **Performance Tracking**: Individual test execution timing
- ✅ **Error Classification**: Distinguishes between failures and errors
- ✅ **Comprehensive Coverage**: Tests core functionality, edge cases, and error conditions
- ✅ **Large Number Testing**: Validates arbitrary precision with very large integers
- ✅ **Cross-base Operations**: Tests mixed base arithmetic operations

### 🧪 Test Coverage Summary

| Test Type | Python Tests | Web Interface Tests | Status |
|-----------|-------------|-------------------|--------|
| **Basic Arithmetic** | ✅ 100% | ✅ 4/4 passing | Complete |
| **Large Numbers** | ✅ Included | ✅ 2/2 passing | Complete |
| **Advanced Math** | ✅ 8 functions | ✅ 4/4 passing | Complete |
| **Base Conversion** | ✅ All bases | ✅ 2/2 passing | Complete |
| **Error Handling** | ✅ Comprehensive | ✅ 2/2 passing | Complete |
| **Performance** | ✅ Timing | ✅ Metrics | Complete |
| **Total Coverage** | **14/14 (100%)** | **14/14 (100%)** | **✅ All Pass** |

Test Interface:
![Test Cases for the API Calculator.](screenshots/tests1.png)

Test Results:
![Test Results for the API Calculator.](screenshots/tests2.png)

## Development Setup

### Prerequisites
- **Python 3.6+** (for CLI and API server)
- **Node.js 16+** (for frontend development)
- **npm or yarn** (package management)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/job-market-analyzer.git
   cd APICalc
   ```

2. **Frontend Development:**
   ```bash
   npm install
   npm run dev
   # Visit http://localhost:3000
   ```

3. **Python CLI:**
   ```bash
   python APICalc.py
   # No dependencies required!
   ```

4. **Full Stack Development:**
   ```bash
   # Install Python API dependencies
   pip install flask flask-cors
   
   # Start both servers
   start_local.bat  # Windows
   # or manually start python api_server.py and npm run dev
   ```

### Build for Production

```bash
npm run build
# Creates optimized build in dist/ folder
```

### Project Structure

```
├── APICalc.py                    # Core Python calculator engine with complex numbers and matrices
├── matrix_operations.py          # Pure implementation of matrix operations
├── app.py                        # Flask web server with REST API endpoints
├── api_server.py                 # Alternative Flask API server (optional)
├── demo_calculator.py            # Demo launcher with auto-browser opening
├── test_web_calculator.py        # Web calculator test suite
├── test_APICalc.py              # Python core test suite
├── test_matrix.py               # Matrix operations test suite
├── final_test.py                 # Comprehensive system tests
├── README_WebInterface.md        # Web interface documentation
├── start_local.bat              # Windows startup script
├── generate_js_calculator.py    # Generate JS from Python
├── templates/
│   └── calculator.html          # Main web interface template
├── static/
│   ├── css/
│   │   └── style.css            # Web interface styling
│   └── js/
│       └── calculator.js        # Frontend JavaScript logic
├── src/
│   ├── components/              # React components
│   │   ├── CalculatorButtons.tsx
│   │   └── Layout.tsx
│   ├── pages/                   # Application pages
│   │   ├── HomePage.tsx
│   │   ├── CalculatorPage.tsx
│   │   └── TestPage.tsx
│   ├── utils/                   # Utility functions
│   │   ├── calculator.ts        # JavaScript calculator
│   │   └── calculator.d.ts      # TypeScript declarations
│   ├── App.tsx                  # Main React application
│   └── main.tsx                # Application entry point
├── public/                      # Static assets
├── screenshots/                 # Demo images
└── package.json                # Node.js dependencies
```

## Architecture

### Core Classes
- `AdvancedPrecisionNumber`: Main number class with arbitrary precision and unary operations
- `ComplexNumber`: Complex number class with full arithmetic and mathematical functions
- `Matrix`: Matrix class supporting arbitrary precision elements and complex matrices
- `CalculatorAPI`: Web API handler for REST endpoints
- `ImprovedTestResult`: Enhanced test result reporting

### Key Methods
- `_parse_input()`: Parse various input formats
- `_base_to_decimal()`: Convert from any base to decimal
- `_decimal_to_base()`: Convert from decimal to any base
- `_standard_multiply()`: Standard multiplication algorithm
- `_karatsuba_multiply()`: Karatsuba multiplication for large numbers
- `_long_division()`: Long division algorithm

## Requirements

### Core Calculator (Python)
- **Python 3.6+**
- **✅ ZERO external dependencies** for core mathematical operations
- **Pure implementation** of all trigonometric, logarithmic, and exponential functions
- **Pure complex number implementation** with all mathematical functions
- Optional modules only for high-precision fallbacks: `decimal` (very large numbers only)

### Web Interface (Frontend)
- **Node.js 16+** (development only)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **TypeScript** support
- **React 18+** with hooks
- **Tailwind CSS** for styling

### Web Interface & API Server
- **Flask** and **Flask-CORS** for web interface and API endpoints
- **Python 3.6+**
- **No additional dependencies** for core functionality

### Deployment
- **Static hosting** (Netlify, Vercel, GitHub Pages) - No server required
- **OR Full stack hosting** (Heroku, AWS, Google Cloud) - For API features

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass (both Python and web interface)
5. Submit a pull request

## Pure Implementation Status

### ✅ **Fully Library-Independent Core Functions**
- **All trigonometric functions**: Pure Taylor series and iterative methods (real and complex)
- **Mathematical constants**: Pi and e calculated using pure iterative methods with caching
- **Exponential and logarithmic functions**: Pure series expansion (real and complex)
- **Complex number operations**: Full complex arithmetic without external libraries
- **Matrix operations**: Complete matrix arithmetic using pure arbitrary precision
- **All arithmetic operations**: Native arbitrary-precision implementation
- **No external library dependencies** for core mathematical operations

### Pure Implementation Details

#### Trigonometric Functions
- **sin(x)**: Taylor series with angle reduction for optimal convergence
- **cos(x)**: Identity relationship with sine function
- **tan(x)**: Calculated as sin(x)/cos(x)
- **arcsin(x)**: Series expansion for small values, Newton's method for larger values
- **arccos(x)**: Identity: arccos(x) = π/2 - arcsin(x)
- **arctan(x)**: Pure Taylor series implementation

#### Mathematical Constants
- **π (Pi)**: Leibniz formula with iterative calculation and caching - π = 4 * Σ((-1)^k / (2k+1))
- **e**: Taylor series - e = Σ(1/n!) for n=0 to infinity
- **Caching system**: Prevents recalculation for commonly used precision levels

#### Algorithms Used
- **Karatsuba multiplication** for large number multiplication
- **Newton-Raphson method** for division and roots
- **Binary exponentiation** for power operations
- **Taylor series expansion** for transcendental functions

## Known Limitations

### Python Implementation
- Very large numbers (>1000 digits) may cause performance issues
- Memory usage grows with precision requirements
- ✅ **All mathematical functions now pure** - No library dependencies
- ✅ **Complex number support fully implemented** - All functions work with complex numbers
- ✅ **Recursion issues resolved** - Iterative algorithms prevent stack overflow

### JavaScript Implementation (React Frontend)
- Limited to JavaScript number precision (~15-17 decimal digits)
- Large factorials (>20!) exceed JavaScript precision
- No complex numbers or advanced mathematical functions
- Cannot handle arbitrary precision like Python version

### Web Interface Implementation (Flask Frontend)
- ✅ **Full arbitrary precision** through Python backend
- ✅ **Complete complex number support** via API integration
- ✅ **All mathematical functions available** through REST endpoints
- ✅ **Real-time calculations** with user-friendly interface

### Deployment
- Static deployment (Netlify) uses JavaScript calculator only
- Full Python precision requires server deployment

## Future Enhancements

### Core Features
- ✅ **Backend API integration** - COMPLETED
- ✅ **Web interface deployment** - COMPLETED
- ✅ **TypeScript integration** - COMPLETED
- ✅ **Complex number support** - COMPLETED
- ✅ **Flask web interface** - COMPLETED
- ✅ **Enhanced REPL** - COMPLETED
- ✅ **Matrix operations** - COMPLETED
- [ ] **Symbolic computation features**

### Advanced Features
- ✅ **Pure arbitrary precision trigonometric functions** (Python) - COMPLETED
- ✅ **Complex number trigonometric functions** (Python) - COMPLETED
- ✅ **Web interface with history and settings** - COMPLETED
- ✅ **REST API endpoints** - COMPLETED
- ✅ **Mathematical constants with caching** - COMPLETED
- [ ] **Pure arbitrary precision trigonometric functions** (JavaScript)
- [ ] **WebAssembly port** for better performance
- [ ] **PWA support** for offline mobile use
- [ ] **Real-time collaboration** features
- [ ] **Calculation session export/import**
- [ ] **Plugin system** for custom functions

### Platform Integrations
- [ ] **Jupyter notebook integration**
- [ ] **VS Code extension**
- [ ] **API marketplace** publishing
- [ ] **Mobile app** (React Native)
