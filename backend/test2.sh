#!/bin/bash
BASE_URL="http://127.0.0.1:8000"
API_URL="${BASE_URL}/api/v1"

echo "==== 1. LOGIN (Get Token) ===="
AUTH_RES=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "test_token"}')
TOKEN=$(echo $AUTH_RES | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')
echo "Token Acquired"

echo -e "\n==== 2. GET COMPANY & USER ===="
COMP_RES=$(curl -s -X GET $API_URL/companies/)
COMP_ID=$(echo $COMP_RES | grep -o '"id":"[^"]*' | head -1 | grep -o '[^"]*$')
USER_RES=$(curl -s -X GET $API_URL/users/)
USER_ID=$(echo $USER_RES | grep -o '"id":"[^"]*' | head -1 | grep -o '[^"]*$')
echo "Company ID: $COMP_ID"
echo "User ID: $USER_ID"

echo -e "\n==== 3. CREATE DEMO SITE ===="
SITE_RES=$(curl -s -X POST $API_URL/sites/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Site Alpha", "address": "Downtown", "latitude": 37.7749, "longitude": -122.4194, "geofence_radius_meters": 100, "company_id": "'$COMP_ID'"}')
echo $SITE_RES
SITE_ID=$(echo $SITE_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 4. GENERATE QR ===="
QR_RES=$(curl -s -X POST $API_URL/sites/$SITE_ID/generate-qr \
  -H "Authorization: Bearer $TOKEN")
echo $QR_RES
QR_TOKEN=$(echo $QR_RES | grep -o '"qr_token":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 5. ASSIGN WORKER ===="
ASSIGN_RES=$(curl -s -X POST $API_URL/sites/$SITE_ID/assign-worker \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"worker_id": "'$USER_ID'"}')
echo $ASSIGN_RES

echo -e "\n==== 6. CHECK IN WORKER ===="
CHECKIN_RES=$(curl -s -X POST $API_URL/attendance/check-in \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_id": "'$SITE_ID'", "qr_token": "'$QR_TOKEN'", "gps_latitude": 37.7750, "gps_longitude": -122.4195}')
echo $CHECKIN_RES

echo -e "\n==== 7. VERIFY OCCUPANCY ===="
OCC_RES=$(curl -s -X GET $API_URL/occupancy/site/$SITE_ID \
  -H "Authorization: Bearer $TOKEN")
echo $OCC_RES

echo -e "\n==== 8. CHECK OUT WORKER ===="
CHECKOUT_RES=$(curl -s -X POST $API_URL/attendance/check-out \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_id": "'$SITE_ID'", "qr_token": "'$QR_TOKEN'", "gps_latitude": 37.7750, "gps_longitude": -122.4195}')
echo $CHECKOUT_RES

echo -e "\n==== 9. VERIFY OCCUPANCY AFTER CHECK OUT ===="
OCC2_RES=$(curl -s -X GET $API_URL/occupancy/site/$SITE_ID \
  -H "Authorization: Bearer $TOKEN")
echo $OCC2_RES
