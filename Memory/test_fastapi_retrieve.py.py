import requests

API_URL = "http://localhost:8000/retrieve"
CONTACT_ID = "test_contact_001"

# Optional: API key header if needed
headers = {
    # "x-api-key": "your-secret-key"
}

def test_fastapi_retrieve():
    print(f"Testing /retrieve for contact_id: {CONTACT_ID}")
    res = requests.get(API_URL, params={"contact_id": CONTACT_ID}, headers=headers)

    print("Status Code:", res.status_code)
    try:
        data = res.json()
        print("Response JSON:", data)
    except Exception as e:
        print("Failed to parse response:", e)

if __name__ == "__main__":
    test_fastapi_retrieve()
