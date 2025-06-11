#!/bin/bash

# test login endpoint
echo "Testing login endpoint..."
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "temp_password_123"}'

echo -e "\n\nTesting refresh token endpoint..."
# first get a token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "temp_password_123"}' | jq -r '.refresh_token')

# then use it to refresh
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\nTesting logout endpoint..."
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN" 