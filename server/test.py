import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print(f"Connecting to FastAPI backend at {BASE_URL}...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] Connection successful!")
            print(f"Server Response: {data}")
            return True
        else:
            print(f"[ERROR] Connection failed. Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection error: Could not reach the server.")
        print(f"Please ensure the backend server is running on {BASE_URL}")
        print("To start the server, run: uvicorn main:app --reload (inside the server directory)")
        return False

if __name__ == "__main__":
    print("=== RAG Medical Agent Verification & Testing ===")
    success = test_health()
    print("==================================================")
    sys.exit(0 if success else 1)
