#!/bin/bash

# test photos upload endpoint implementation

# generate unique timestamps for emails
TIMESTAMP=$(date +%s)

# first create a test user and get auth token
echo "Creating test user and getting auth token..."
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"test${TIMESTAMP}@example.com\",
    \"password\": \"testpassword123\"
  }")

USER_ID=$(echo $AUTH_RESPONSE | jq -r '.user_id')
TOKEN=$(echo $AUTH_RESPONSE | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "Failed to get auth token. Creating new user first..."
    # Create user first
    curl -s -X POST http://localhost:8000/users/register \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"test${TIMESTAMP}@example.com\",
        \"full_name\": \"Test User\",
        \"password\": \"testpassword123\"
      }"
    
    # Then login to get token
    AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/login \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"test${TIMESTAMP}@example.com\",
        \"password\": \"testpassword123\"
      }")
    
    USER_ID=$(echo $AUTH_RESPONSE | jq -r '.user_id')
    TOKEN=$(echo $AUTH_RESPONSE | jq -r '.access_token')
fi

echo "Created test user with ID: $USER_ID"
echo "Got auth token: $TOKEN"

# test 1: upload photo with valid data
echo -e "\nTest 1: Uploading photo with valid data..."
curl -X POST http://localhost:8000/photos/upload \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"photo_url\": \"https://example.com/test-photo.jpg\",
    \"notes\": \"Test photo entry\"
  }"

# test 2: upload photo with invalid URL
echo -e "\nTest 2: Uploading photo with invalid URL..."
curl -X POST http://localhost:8000/photos/upload \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"photo_url\": \"not-a-valid-url\",
    \"notes\": \"Test photo entry\"
  }"

# test 3: upload photo without auth token
echo -e "\nTest 3: Uploading photo without auth token..."
curl -X POST http://localhost:8000/photos/upload \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"photo_url\": \"https://example.com/test-photo.jpg\",
    \"notes\": \"Test photo entry\"
  }"

# test 4: upload photo for different user
echo -e "\nTest 4: Uploading photo for different user..."
curl -X POST http://localhost:8000/photos/upload \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"user_id\": \"00000000-0000-0000-0000-000000000000\",
    \"photo_url\": \"https://example.com/test-photo.jpg\",
    \"notes\": \"Test photo entry\"
  }"

# test 5: verify photos were created
echo -e "\nTest 5: Verifying photos were created..."
curl -X GET http://localhost:8000/photos/$USER_ID \
  -H "Authorization: Bearer $TOKEN" 