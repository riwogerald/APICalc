#!/usr/bin/env python
"""Debug script to identify recursion issue"""

import sys
import traceback

# Set lower recursion limit to catch the issue faster
sys.setrecursionlimit(100)

try:
    from APICalc import AdvancedPrecisionNumber
    print("Successfully imported AdvancedPrecisionNumber")
    
    # Try to create a simple number
    print("Creating AdvancedPrecisionNumber('1')...")
    num = AdvancedPrecisionNumber('1')
    print(f"Success: Created {num}")
    
    # Try to call sin() which uses _get_pi internally
    print("Calling num.sin()...")
    result = num.sin()
    print(f"Success: sin(1) = {result}")
    
except RecursionError as e:
    print("RecursionError occurred!")
    traceback.print_exc(limit=15)
except Exception as e:
    print(f"Other error occurred: {e}")
    traceback.print_exc()
