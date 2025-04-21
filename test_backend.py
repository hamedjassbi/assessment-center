import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Create .env file with placeholder for OpenAI API key
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('OPENAI_API_KEY=your_openai_api_key_here\n')
    print("Created .env file with placeholder for OpenAI API key")

# Test script to verify the backend functionality
if __name__ == "__main__":
    import requests
    import json
    import time
    
    # Configuration
    BASE_URL = "http://localhost:8080"  # Change if using a different port
    
    def test_health_check():
        print("\n=== Testing Health Check Endpoint ===")
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check successful")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error during health check: {str(e)}")
            return False
    
    def test_start_quiz():
        print("\n=== Testing Start Quiz Endpoint ===")
        try:
            payload = {"test": "IQ Test"}
            response = requests.post(f"{BASE_URL}/start", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Start quiz successful")
                print(f"Thread ID: {data.get('thread_id')}")
                print(f"Question: {data.get('question')}")
                print(f"Options count: {len(data.get('options', []))}")
                return data.get('thread_id')
            else:
                print(f"❌ Start quiz failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error during start quiz: {str(e)}")
            return None
    
    def test_quiz_response(thread_id):
        print("\n=== Testing Quiz Response Endpoint ===")
        if not thread_id:
            print("❌ Cannot test quiz response without thread ID")
            return False
        
        try:
            payload = {
                "thread_id": thread_id,
                "message": "Option A"  # Generic response
            }
            response = requests.post(f"{BASE_URL}/quiz", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Quiz response successful")
                print(f"Question: {data.get('question')}")
                print(f"Options count: {len(data.get('options', []))}")
                print(f"Is results: {data.get('is_results', False)}")
                return True
            else:
                print(f"❌ Quiz response failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error during quiz response: {str(e)}")
            return False
    
    # Run tests
    print("Starting backend tests...")
    
    # Check if OpenAI API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("⚠️ Warning: OPENAI_API_KEY is not set or using placeholder value")
        print("Tests may fail without a valid API key")
    
    # Run the tests
    health_ok = test_health_check()
    
    if health_ok:
        thread_id = test_start_quiz()
        if thread_id:
            test_quiz_response(thread_id)
    
    print("\nTests completed")
