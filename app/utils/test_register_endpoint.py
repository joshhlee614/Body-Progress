import asyncio
import httpx
import os
from dotenv import load_dotenv
import json

load_dotenv()

async def test_register_endpoint():
    # get the base url from environment
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    endpoint = f"{base_url}/users/register"
    # test data
    test_email = f"test_{int(asyncio.get_event_loop().time())}@example.com"
    test_full_name = "Test User"
    payload = {"email": test_email, "full_name": test_full_name}
    print(f"Testing user registration with URL: {endpoint}")
    print(f"Payload: {json.dumps(payload)}")
    headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Registration successful")
            print(f"Response data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_register_endpoint()) 