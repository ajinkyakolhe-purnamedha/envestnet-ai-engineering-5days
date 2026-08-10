# Call an API
import requests

try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    print(response.json())
except requests.RequestException:
    print("Local API is unavailable")

