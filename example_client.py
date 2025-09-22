#!/usr/bin/env python3
"""
Example client for Simple Chat AI API
This script demonstrates how to interact with the chat API
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def chat_example():
    """Example chat interaction"""
    print("\nTesting chat endpoint...")
    
    # Simple question
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is artificial intelligence?"}
    ]
    
    payload = {
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['message']}")
            if result.get('usage'):
                print(f"Token Usage: {result['usage']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Chat request failed: {e}")

def conversation_example():
    """Example multi-turn conversation"""
    print("\nTesting conversation with context...")
    
    messages = [
        {"role": "system", "content": "You are a helpful programming assistant."},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991."},
        {"role": "user", "content": "What makes it popular for beginners?"}
    ]
    
    payload = {
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['message']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Conversation request failed: {e}")

def main():
    """Run example tests"""
    print("Simple Chat AI API - Example Client")
    print("=" * 40)
    
    # Test health first
    if not test_health():
        print("Health check failed. Make sure the server is running and configured properly.")
        sys.exit(1)
    
    # Run chat examples
    chat_example()
    conversation_example()
    
    print("\nExample completed!")

if __name__ == "__main__":
    main()