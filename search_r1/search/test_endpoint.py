import requests

def test_retrieve_endpoint():
    url = "http://127.0.0.1:8000/retrieve"
    payload = {
        "queries": ["What is Python?", "Tell me about neural networks."],
        "topk": 3,
        "return_scores": True
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())


if __name__ == "__main__":
    test_retrieve_endpoint()