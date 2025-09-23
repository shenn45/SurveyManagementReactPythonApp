#!/usr/bin/env python3
"""
Simple test script to verify debugpy and VS Code debugging setup
"""

def test_function():
    """Test function for debugging"""
    message = "Hello from debugpy test!"
    print(message)
    
    # Set a breakpoint here to test debugging
    result = 1 + 1
    print(f"1 + 1 = {result}")
    
    return result

if __name__ == "__main__":
    print("Starting debugpy test...")
    
    # Test debugpy import
    try:
        import debugpy
        print(f"✓ debugpy successfully imported, version: {debugpy.__version__}")
        print(f"✓ debugpy location: {debugpy.__file__}")
    except ImportError as e:
        print(f"✗ Failed to import debugpy: {e}")
        exit(1)
    
    # Test function call
    result = test_function()
    print(f"Test completed successfully! Result: {result}")