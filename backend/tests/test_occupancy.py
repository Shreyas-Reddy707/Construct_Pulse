def test_occupancy_current(client, setup_data):
    response = client.get(
        "/api/v1/occupancy/current",
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 200

def test_occupancy_site(client, setup_data):
    response = client.get(
        f"/api/v1/occupancy/site/{setup_data['site_id']}",
        headers={"Authorization": f"Bearer {setup_data['token']}"}
    )
    assert response.status_code == 200
    assert "total_workers" in response.json()
