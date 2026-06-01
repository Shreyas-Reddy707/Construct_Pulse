def test_check_in_success(client, setup_data):
    response = client.post(
        "/api/v1/attendance/check-in",
        json={"site_id": setup_data["site_id"], "qr_token": setup_data["qr_token"], "gps_latitude": 10.0, "gps_longitude": 10.0},
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "checked_in"

def test_check_in_duplicate(client, setup_data):
    response = client.post(
        "/api/v1/attendance/check-in",
        json={"site_id": setup_data["site_id"], "qr_token": setup_data["qr_token"], "gps_latitude": 10.0, "gps_longitude": 10.0},
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 400
    assert "active check-in" in response.json()["detail"]

def test_check_out_success(client, setup_data):
    response = client.post(
        "/api/v1/attendance/check-out",
        json={"site_id": setup_data["site_id"], "qr_token": setup_data["qr_token"], "gps_latitude": 10.0, "gps_longitude": 10.0},
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "checked_out"

def test_check_out_without_active(client, setup_data):
    response = client.post(
        "/api/v1/attendance/check-out",
        json={"site_id": setup_data["site_id"], "qr_token": setup_data["qr_token"], "gps_latitude": 10.0, "gps_longitude": 10.0},
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 404
    assert "Active check-in not found" in response.json()["detail"]
