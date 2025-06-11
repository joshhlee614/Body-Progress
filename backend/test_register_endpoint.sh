#!/bin/bash

EMAIL="test_$(date +%s)@example.com"
FULL_NAME="Shell Script User"

JSON_PAYLOAD=$(cat <<EOF
{
  "email": "$EMAIL",
  "full_name": "$FULL_NAME"
}
EOF
)

RESPONSE=$(curl -s -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

echo "Testing user registration with email: $EMAIL"
echo "Response: $RESPONSE" 