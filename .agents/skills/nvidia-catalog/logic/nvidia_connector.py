import os
import requests
import json
from dotenv import load_dotenv

# Load NEXUS global environment
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../../.env"))

class NVIDIAConnector:
    """
    NEXUS Core Connector for NVIDIA API Catalog.
    Provides a standardized interface for all NEXUS agents to access high-parameter models.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            # Fallback for local testing
            self.api_key = os.getenv("LOCAL_NVIDIA_KEY")
            
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in NEXUS environment.")
        
        self.base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def chat(self, model="meta/llama-3.1-405b-instruct", messages=None, temperature=0.2, max_tokens=2048):
        """
        Standardized chat completion for NEXUS agents.
        """
        if messages is None:
            return "ERROR: No messages provided to NVIDIAConnector."
            
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": 0.7,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"ERROR: [NVIDIA_CONNECTOR] {str(e)}"

if __name__ == "__main__":
    # Internal NEXUS Diagnostic
    connector = NVIDIAConnector()
    print(f"NEXUS Diagnostic: Calling {connector.base_url}")
    print(connector.chat(messages=[{"role": "user", "content": "NEXUS Integration Test. Confirm status."}]))
