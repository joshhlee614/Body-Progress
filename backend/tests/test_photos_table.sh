#!/bin/bash

# test photos table implementation

# generate unique timestamps for emails
TIMESTAMP=$(date +%s)

# first create a test user
echo "Creating test user..."
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"test${TIMESTAMP}@example.com\",
    \"full_name\": \"Test User\",
    \"password\": \"testpassword123\"
  }"

# store the user id from response
USER_ID=$(curl -s http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"test2${TIMESTAMP}@example.com\",
    \"full_name\": \"Test User 2\",
    \"password\": \"testpassword123\"
  }" | jq -r '.id')

echo "Created test user with ID: $USER_ID"

# create a test photo entry
echo "Creating test photo entry..."
curl -X POST http://localhost:8000/photos/upload \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"photo_url\": \"https://example.com/test-photo.jpg\",
    \"notes\": \"Test photo entry\"
  }"

# verify the photo was created
echo "Verifying photo entry..."
curl -X GET http://localhost:8000/photos/$USER_ID 