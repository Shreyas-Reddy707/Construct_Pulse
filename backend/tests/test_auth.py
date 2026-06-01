def test_login_invalid_token(client):
    response = client.post("/api/v1/auth/login", json={"token": "invalid_token"})
    assert response.status_code == 401
    assert "Invalid Firebase token" in response.json()["detail"]

def test_login_integration_token(client, setup_data):
    # Should work due to integration_ token bypass
    response = client.post("/api/v1/auth/login", json={"token": f"integration_{setup_data['firebase_uid']}"})
    assert response.status_code == 401 # Wait, we removed this bypass, so it should be 401 now!
    assert "Invalid Firebase token" in response.json()["detail"]
