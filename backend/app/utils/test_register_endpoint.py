import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import json

load_dotenv()

async def test_register_endpoint():
    # get the base url from environment
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # test data
    test_email = f"test_{int(asyncio.get_event_loop().time())}@example.com"
    
    print(f"Testing user registration with email: {test_email}")
    
    async with aiohttp.ClientSession() as session:
        # test registration
        async with session.post(
            f"{base_url}/users/register",
            json={"email": test_email}
        ) as response:
            if response.status == 200:
                data = await response.json()
                print("✅ Registration successful")
                print(f"Response data: {json.dumps(data, indent=2)}")
            else:
                error = await response.text()
                print(f"❌ Registration failed with status {response.status}")
                print(f"Error: {error}")

if __name__ == "__main__":
    asyncio.run(test_register_endpoint()) 