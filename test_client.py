#!/usr/bin/env python3
"""
Simple test client for the Facehug Chat API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.json()}")
    return response.status_code == 200

def test_chat(message):
    """Test chat endpoint"""
    data = {
        "message": message,
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"User: {message}")
        print(f"Bot: {result['response']}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

def main():
    print("Testing Facehug Chat API...")
    
    # Test health
    if not test_health():
        print("Health check failed!")
        return
    
    # Test chat
    test_messages = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me a joke"
    ]
    
    for message in test_messages:
        print("\n" + "="*50)
        test_chat(message)

if __name__ == "__main__":
    main()