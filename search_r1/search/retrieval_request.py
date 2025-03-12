'''
python search_r1/search/retrieval_request.py
'''

import requests

# URL for your local FastAPI server
url = "http://127.0.0.1:8000/retrieve"

# Example payload
payload = {
    "queries": ["What is the capital of France?"],
    "topk": 5,
    "return_scores": True
}

# Send POST request
response = requests.post(url, json=payload)

# Raise an exception if the request failed
response.raise_for_status()

# Get the JSON response
retrieved_data = response.json()

print("Response from server:")
print(retrieved_data)
