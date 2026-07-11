import requests
import json

base_url = "http://localhost:8000/api/v1"
phone = "+10000000000"

print("1. Testing POST /auth/login...")
login_payload = {"token": f"DEMO_TOKEN_{phone}"}
response = requests.post(f"{base_url}/auth/login", json=login_payload)
print(f"Status: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text}")
    exit(1)

data = response.json()
access_token = data.get("access_token")
print(f"Received access_token: {access_token[:20]}...")

headers = {"Authorization": f"Bearer {access_token}"}

print("\n2. Testing GET /dashboard/metrics...")
r1 = requests.get(f"{base_url}/dashboard/metrics", headers=headers)
print(f"Metrics Status: {r1.status_code}")

print("\n3. Testing GET /dashboard/recent-activity...")
r2 = requests.get(f"{base_url}/dashboard/recent-activity", headers=headers)
print(f"Activity Status: {r2.status_code}")

print("\n4. Testing GET /dashboard/trends...")
# Trends needs start_date and end_date
r3 = requests.get(f"{base_url}/dashboard/trends?start_date=2026-07-01T00:00:00Z&end_date=2026-07-31T00:00:00Z", headers=headers)
print(f"Trends Status: {r3.status_code}")

if r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
    print("\nSUCCESS: All endpoints return 200 OK. The AuthSession was successfully committed and authorized.")
else:
    print("\nFAILURE: One or more endpoints failed.")
