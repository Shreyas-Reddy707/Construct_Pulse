import sys
import uuid
from fastapi.testclient import TestClient
from main import app

def run():
    client = TestClient(app)
    
    # 1. Fetch departments via public endpoint
    print("Fetching public departments...")
    dept_response = client.get("/api/v1/public/departments")
    if dept_response.status_code != 200:
        print(f"Failed to fetch departments: {dept_response.text}")
        sys.exit(1)
    departments = dept_response.json()
    print(f"Found {len(departments)} departments")
    if not departments:
        print("No departments available. Please ensure db is seeded.")
        sys.exit(1)
        
    dept_id = departments[0]['id']
    
    # 2. Fetch contractors via public endpoint
    print("Fetching public contractors...")
    cont_response = client.get("/api/v1/public/contractors")
    if cont_response.status_code != 200:
        print(f"Failed to fetch contractors: {cont_response.text}")
        sys.exit(1)
    contractors = cont_response.json()
    print(f"Found {len(contractors)} contractors")
    cont_id = contractors[0]['id'] if contractors else None
    
    # 3. Submit Registration
    new_phone = f"+1555{uuid.uuid4().hex[:7]}"
    print(f"Registering new worker with phone {new_phone}...")
    
    register_payload = {
        "first_name": "Fix",
        "last_name": "Tester",
        "phone": new_phone,
        "department_id": dept_id,
        "contractor_id": cont_id,
        "designation": "Plumber",
        "emergency_contact_name": "Bob",
        "emergency_contact_phone": "+19999999999"
    }
    
    reg_response = client.post("/api/v1/auth/register", json=register_payload)
    if reg_response.status_code != 200:
        print(f"Registration failed: {reg_response.text}")
        sys.exit(1)
        
    print(f"Registration successful: {reg_response.json()}")

if __name__ == "__main__":
    run()
