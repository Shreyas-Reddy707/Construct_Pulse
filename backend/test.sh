#!/bin/bash
BASE_URL="http://127.0.0.1:8000"
API_URL="${BASE_URL}/api/v1"

echo "1. GET /"
curl -s $BASE_URL/
echo -e "\n"

echo "2. POST /users"
USER_RES=$(curl -s -X POST $API_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "name": "Admin User", "role": "System Admin", "firebase_uid": "test_firebase_uid"}')
echo $USER_RES
echo -e "\n"

echo "3. POST /auth/login"
AUTH_RES=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "test_token"}')
echo $AUTH_RES
echo -e "\n"

TOKEN=$(echo $AUTH_RES | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')

echo "4. POST /companies"
COMP_RES=$(curl -s -X POST $API_URL/companies/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "ConstructPulse Inc", "address": "123 Main St", "phone": "555-0100"}')
echo $COMP_RES
echo -e "\n"

COMP_ID=$(echo $COMP_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo "5. POST /departments"
DEPT_RES=$(curl -s -X POST $API_URL/departments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering", "description": "Core engineering team", "company_id": "'$COMP_ID'"}')
echo $DEPT_RES
echo -e "\n"

echo "6. POST /contractors"
CONT_RES=$(curl -s -X POST $API_URL/contractors/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "BuildIt Contractors", "phone": "555-0200", "trade": "Plumbing", "company_id": "'$COMP_ID'"}')
echo $CONT_RES
echo -e "\n"

echo "7. GET /companies"
GET_COMP_RES=$(curl -s -X GET $API_URL/companies/)
echo $GET_COMP_RES
echo -e "\n"
