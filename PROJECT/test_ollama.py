import requests
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:3b",
        "prompt": "What is NEXUS?",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("\n[OLLAMA QWEN2.5-CODER OUTPUT]:\n")
            print(response.json().get("response"))
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to Ollama: {e}")

if __name__ == "__main__":
    test_ollama()
