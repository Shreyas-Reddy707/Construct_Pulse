#!/bin/bash
BASE_URL="http://127.0.0.1:8000/api/v1"

echo "==== 1. LOGIN (Auth Module) ===="
AUTH_RES=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "integration_test_firebase_token"}')
echo $AUTH_RES
TOKEN=$(echo $AUTH_RES | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')

# Ensure we have a token
if [ -z "$TOKEN" ]; then
  echo "Login failed!"
  exit 1
fi

echo -e "\n==== 2. WORKER REGISTRATION (Auth Module) ===="
USER_RES=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1999888777", "name": "Integration Worker", "role": "Worker", "firebase_uid": "integration_uid_123"}')
echo $USER_RES
WORKER_ID=$(echo $USER_RES | grep -o '"id":"[^"]*' | head -1 | grep -o '[^"]*$')
if [ -z "$WORKER_ID" ]; then
  # Fallback to an existing user if phone already registered
  USER_RES=$(curl -s -X GET $BASE_URL/users/ | grep -o '"id":"[^"]*' | head -1)
  WORKER_ID=$(echo $USER_RES | grep -o '[^"]*$')
fi
echo "Worker ID: $WORKER_ID"

echo -e "\n==== 3. CREATE COMPANY (Company Module) ===="
COMP_RES=$(curl -s -X POST $BASE_URL/companies/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "ConstructPulse Global", "address": "456 Enterprise Way", "phone": "555-9000"}')
echo $COMP_RES
COMP_ID=$(echo $COMP_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 4. CREATE DEPARTMENT (Department Module) ===="
DEPT_RES=$(curl -s -X POST $BASE_URL/departments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Civil Engineering", "description": "Core civil works", "company_id": "'$COMP_ID'"}')
echo $DEPT_RES
DEPT_ID=$(echo $DEPT_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 5. CREATE CONTRACTOR (Contractor Module) ===="
CONT_RES=$(curl -s -X POST $BASE_URL/contractors/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "SteelWorks LLC", "phone": "555-8000", "trade": "Steel", "company_id": "'$COMP_ID'"}')
echo $CONT_RES
CONT_ID=$(echo $CONT_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 6. CREATE SITE (Site Module) ===="
SITE_RES=$(curl -s -X POST $BASE_URL/sites/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Integration Site Omega", "address": "Uptown", "latitude": 37.7800, "longitude": -122.4200, "geofence_radius_meters": 150, "company_id": "'$COMP_ID'"}')
echo $SITE_RES
SITE_ID=$(echo $SITE_RES | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

# Assign worker to site so check-in works
curl -s -X POST $BASE_URL/sites/$SITE_ID/assign-worker \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"worker_id": "'$WORKER_ID'"}' > /dev/null

echo -e "\n==== 7. GENERATE QR (QR Module) ===="
QR_RES=$(curl -s -X POST $BASE_URL/sites/$SITE_ID/generate-qr \
  -H "Authorization: Bearer $TOKEN")
echo $QR_RES
QR_TOKEN=$(echo $QR_RES | grep -o '"qr_token":"[^"]*' | grep -o '[^"]*$')

echo -e "\n==== 8. CHECK IN (Attendance Module) ===="
# Login as the worker to check in
WORKER_AUTH=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "integration_uid_123"}')
WORKER_TOKEN=$(echo $WORKER_AUTH | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')

CHECKIN_RES=$(curl -s -X POST $BASE_URL/attendance/check-in \
  -H "Authorization: Bearer $WORKER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_id": "'$SITE_ID'", "qr_token": "'$QR_TOKEN'", "gps_latitude": 37.7800, "gps_longitude": -122.4200}')
echo $CHECKIN_RES

echo -e "\n==== 9. OCCUPANCY DASHBOARD (Occupancy Module) ===="
OCC_RES=$(curl -s -X GET $BASE_URL/occupancy/site/$SITE_ID \
  -H "Authorization: Bearer $TOKEN")
echo $OCC_RES

echo -e "\n==== 10. CHECK OUT (Attendance Module) ===="
CHECKOUT_RES=$(curl -s -X POST $BASE_URL/attendance/check-out \
  -H "Authorization: Bearer $WORKER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_id": "'$SITE_ID'", "qr_token": "'$QR_TOKEN'", "gps_latitude": 37.7800, "gps_longitude": -122.4200}')
echo $CHECKOUT_RES

echo -e "\n==== 11. OCCUPANCY AFTER CHECKOUT ===="
OCC2_RES=$(curl -s -X GET $BASE_URL/occupancy/site/$SITE_ID \
  -H "Authorization: Bearer $TOKEN")
echo $OCC2_RES
