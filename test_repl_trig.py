#!/usr/bin/env python3

import subprocess
import time

def test_repl_trigonometric():
    print("Testing REPL trigonometric functions...")
    
    # Test expressions to send to the REPL
    test_expressions = [
        "sin(1.5708)",
        "cos(0)",
        "tan(0.7854)",
        "Sin(90)",  # This was the failing case
        "quit"
    ]
    
    # Start the calculator process
    proc = subprocess.Popen(
        ['python', 'APICalc.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Send commands and collect output
        output_lines = []
        for expr in test_expressions:
            print(f"Sending: {expr}")
            proc.stdin.write(f"{expr}\n")
            proc.stdin.flush()
            time.sleep(0.1)  # Small delay to let the process respond
        
        # Wait for the process to complete
        stdout, stderr = proc.communicate(timeout=5)
        
        print("STDOUT:")
        print(stdout)
        if stderr:
            print("STDERR:")
            print(stderr)
            
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        print("Process timed out")
        print("STDOUT:")
        print(stdout)
        if stderr:
            print("STDERR:")
            print(stderr)

if __name__ == "__main__":
    test_repl_trigonometric()
