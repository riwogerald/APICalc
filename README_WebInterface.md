# Advanced Precision Calculator - Web Interface

A beautiful, feature-rich web interface for the Advanced Precision Calculator, providing high-precision arithmetic with complex number support directly in your browser.

## 🚀 Features

### Core Capabilities
- **High-Precision Arithmetic**: Support for 50, 200, or 1000+ digit precision
- **Complex Number Support**: Full complex arithmetic (3+4i, 2-5j, etc.)
- **Multiple Number Bases**: Binary, octal, decimal, and hexadecimal
- **Mathematical Functions**: Trigonometry, logarithms, roots, and more
- **Real-time Calculations**: Instant results with comprehensive error handling

### Web Interface Features
- **Modern UI**: Responsive design that works on desktop and mobile
- **Calculation History**: Save and recall previous calculations
- **Advanced Panel**: Quick access to specialized functions
- **Keyboard Shortcuts**: Efficient input with hotkeys
- **Settings Panel**: Configure precision, base, and display options
- **Error Handling**: User-friendly error messages and validation

## 🎯 Quick Start

### Prerequisites
```bash
pip install flask flask-cors
```

### Running the Calculator

#### Option 1: Demo Mode (Recommended for first-time users)
```bash
python demo_calculator.py
```
This will:
- Display feature overview and examples
- Start the web server automatically
- Open your browser to the calculator interface

#### Option 2: Direct Server Start
```bash
python app.py
```
Then open your browser to: `http://localhost:5000`

#### Option 3: Test Mode (Verify functionality)
```bash
python test_web_calculator.py
```

## 🧮 Using the Calculator

### Basic Operations
- **Arithmetic**: `123 + 456`, `999 * 888`, `22 / 7`
- **Powers**: `2 ** 100`, `3 ** 0.5`
- **Parentheses**: `(2 + 3) * (4 - 1)`

### Complex Numbers
- **Creation**: `3+4i`, `2-5j`, `7i`, `-3i`
- **Arithmetic**: `(3+4i) + (1-2i)`, `(2+3i) * (1-i)`
- **Functions**: `abs(3+4i)`, `conjugate(2-5i)`, `arg(1+i)`

### Mathematical Functions
Click function buttons or type directly:
- **Trigonometry**: `sin(1.57)`, `cos(3.14)`, `tan(0.785)`
- **Inverse Trig**: `arcsin(0.5)`, `arccos(0.707)`, `arctan(1)`
- **Logarithms**: `log(10)`, `log(100, 10)`, `exp(2)`
- **Roots**: `sqrt(2)`, `cube_root(27)`
- **Special**: `factorial(10)`, `inverse(5)`

### Constants
- **π (Pi)**: Click the π button or type `pi`
- **e (Euler's number)**: Click the e button or type `e`

### Number Bases
Change the base in settings:
- **Binary**: `0b1010` (displays as binary)
- **Octal**: `0o755` (displays as octal)  
- **Hexadecimal**: `0xFF` (displays as hex)

## 🎨 Interface Guide

### Main Areas

1. **Display Section**
   - Expression display: Shows current input
   - Result display: Shows calculation results
   - Settings bar: Precision, base, and mode controls

2. **Input Section**
   - Text input field for expressions
   - Calculate button (or press Enter)

3. **Button Grid**
   - Numbers and basic operators
   - Mathematical functions
   - Constants and special operations

4. **Advanced Panel** (toggle to show/hide)
   - Specialized functions (cube, cube root, etc.)
   - Complex number examples
   - Additional mathematical operations

5. **History Panel** (toggle to show/hide)
   - View previous calculations
   - Click any history item to reuse it
   - Clear history option

6. **Status Bar**
   - Current mode (Real/Complex)
   - Number base and precision settings
   - Connection status to backend

### Keyboard Shortcuts

- **Enter**: Calculate current expression
- **Ctrl+Enter**: Calculate (alternative)
- **Ctrl+Backspace**: Clear all
- **Ctrl+H**: Toggle history panel
- **Ctrl+M**: Toggle complex mode
- **Escape**: Close modals/panels

## 🔧 API Endpoints

The web interface communicates with the backend through REST API:

### `/api/calculate` (POST)
Calculate mathematical expressions
```json
{
  "expression": "3 + 4 * 5",
  "precision_mode": "standard",
  "base": 10
}
```

### `/api/function` (POST)
Execute mathematical functions
```json
{
  "function": "sin",
  "args": ["1.57"],
  "precision_mode": "standard",
  "base": 10
}
```

### `/api/constants` (GET)
Get mathematical constants
```
GET /api/constants?precision=25
```

### `/api/convert_base` (POST)
Convert between number bases
```json
{
  "value": "255",
  "from_base": 10,
  "to_base": 16
}
```

## 🎛️ Configuration Options

### Precision Modes
- **Standard**: 50 digits (fast, suitable for most calculations)
- **High**: 200 digits (more precise, slower)
- **Extreme**: 1000 digits (maximum precision, slowest)

### Number Bases
- **Decimal (10)**: Standard base-10 numbers
- **Binary (2)**: Binary representation (0b prefix)
- **Octal (8)**: Octal representation (0o prefix)
- **Hexadecimal (16)**: Hex representation (0x prefix)

### Display Modes
- **Real Mode**: Standard real number calculations
- **Complex Mode**: Shows complex number indicators

## 📝 Examples

### High-Precision Calculations
```
Input: 22 / 7
Output: 3.1428571428571428571428571428571428571428571428571

Input: sqrt(2)
Output: 1.4142135623730950488016887242096980785831761566772
```

### Complex Number Operations
```
Input: 3+4i
Output: 3+4i

Input: abs(3+4i)
Output: 5

Input: sin(1+2i)
Output: 3.165778513216168+1.959601041421606i
```

### Advanced Functions
```
Input: factorial(20)
Output: 2432902008176640000

Input: log(exp(5))
Output: 5

Input: conjugate(3-4i)
Output: 3+4i
```

## 🛠️ Development

### File Structure
```
APICalc/
├── app.py                 # Flask web server and API
├── APICalc.py            # Core calculation engine
├── templates/
│   └── calculator.html   # Main web interface
├── static/
│   ├── css/
│   │   └── style.css    # Interface styling
│   └── js/
│       └── calculator.js # Frontend logic
├── demo_calculator.py    # Demo launcher
├── test_web_calculator.py # Test suite
└── README_WebInterface.md # This file
```

### Backend API (`app.py`)
- Flask web server
- RESTful API endpoints
- Expression parsing and evaluation
- Error handling and validation

### Frontend (`calculator.html`, `style.css`, `calculator.js`)
- Responsive web interface
- Real-time calculation updates
- History management
- Settings persistence

### Core Engine (`APICalc.py`)
- High-precision arithmetic
- Complex number support
- Mathematical functions
- Multiple number bases

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python test_web_calculator.py
```

This tests:
- Basic arithmetic operations
- Complex number handling
- Mathematical functions
- Number base conversions
- API endpoint functionality

## 🚀 Deployment

### Development Server
```bash
python app.py
```

### Production Deployment
For production, use a proper WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is part of the Advanced Precision Calculator suite. See the main project documentation for licensing information.

## 🔗 Related

- **Core Engine**: `APICalc.py` - The mathematical calculation engine
- **CLI Interface**: `calculate_repl()` - Command-line interface
- **Test Suite**: Various test files for verification

---

**Happy Calculating! 🧮✨**
