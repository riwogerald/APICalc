#!/usr/bin/env python3
"""
Demo script for the Advanced Precision Calculator Web Interface
Shows the calculator capabilities in action
"""

import sys
import time
import threading
import webbrowser
from app import app

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("🧮 ADVANCED PRECISION CALCULATOR - WEB INTERFACE DEMO 🧮")
    print("=" * 70)
    print()
    print("🚀 Features:")
    print("   • High-precision arithmetic (50, 200, or 1000 digits)")
    print("   • Complex number support (3+4i, 2-5j, etc.)")
    print("   • Mathematical functions (sin, cos, sqrt, log, etc.)")
    print("   • Multiple number bases (binary, octal, decimal, hex)")
    print("   • Interactive web interface with history")
    print("   • Real-time calculations with error handling")
    print()

def demo_calculations():
    """Show example calculations"""
    print("📊 Example Calculations You Can Try:")
    print()
    
    examples = [
        ("Basic Arithmetic", [
            "123 + 456",
            "999 * 888",
            "22 / 7",
            "2 ** 100"
        ]),
        ("Complex Numbers", [
            "3+4i",
            "2-3i",
            "(3+4i) + (1-2i)",
            "abs(3+4i)"
        ]),
        ("Mathematical Functions", [
            "sin(1.57)",
            "cos(3.14159)",
            "sqrt(2)",
            "log(10)",
            "factorial(10)"
        ]),
        ("Advanced Operations", [
            "sin(3+4i)",
            "sqrt(-1)",
            "exp(2+3i)",
            "conjugate(5-7i)"
        ])
    ]
    
    for category, calcs in examples:
        print(f"   {category}:")
        for calc in calcs:
            print(f"     • {calc}")
        print()

def open_browser_delayed():
    """Open browser after a short delay"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Browser opened automatically!")
    except:
        print("⚠️  Could not open browser automatically.")
        print("   Please manually open: http://localhost:5000")

def main():
    """Main demo function"""
    print_banner()
    demo_calculations()
    
    print("🔧 Starting Web Server...")
    print("   Server will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print()
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Start the Flask development server
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Calculator server stopped. Goodbye!")
        return True
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
