#!/bin/bash

# test login endpoint
echo "Testing login endpoint..."
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "temp_password_123"}' | jq

echo -e "\n\nTesting login with invalid credentials..."
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "wrong_password"}' | jq 