#!/usr/bin/env python3
"""
Test script to verify API server connectivity
"""
import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API Server Connectivity...")
    print(f"📡 Base URL: {base_url}")
    
    # Test health endpoint
    try:
        print("\n1. Testing Health Endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Health check passed!")
        else:
            print("   ❌ Health check failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error: Cannot connect to API server")
        print("   💡 Make sure the API server is running: python api_server.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test calculation endpoint
    try:
        print("\n2. Testing Calculation Endpoint...")
        test_data = {"expression": "123 + 456"}
        response = requests.post(
            f"{base_url}/api/calculate", 
            json=test_data,
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        
        if response.status_code == 200 and result.get('success'):
            print(f"   ✅ Calculation test passed! Result: {result.get('result')}")
        else:
            print("   ❌ Calculation test failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test advanced function
    try:
        print("\n3. Testing Advanced Function...")
        test_data = {"expression": "factorial(5)"}
        response = requests.post(
            f"{base_url}/api/calculate", 
            json=test_data,
            timeout=5
        )
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Response: {result}")
        
        if response.status_code == 200 and result.get('success'):
            print(f"   ✅ Advanced function test passed! Result: {result.get('result')}")
        else:
            print("   ❌ Advanced function test failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n🎉 All API tests passed! The server is working correctly.")
    return True

if __name__ == "__main__":
    success = test_api()
    if not success:
        print("\n🔧 Troubleshooting Tips:")
        print("1. Make sure the API server is running: python api_server.py")
        print("2. Check if port 5000 is available")
        print("3. Verify Flask and Flask-CORS are installed: pip install flask flask-cors")
        print("4. Try restarting the API server")
