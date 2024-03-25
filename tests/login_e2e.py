import pytest,httpx


# Define the base URL of your FastAPI application
base_url = "http://localhost:8000/api"

# Test login endpoint
@pytest.mark.asyncio
async def test_login():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/token", json={"username": "admin", "password": "adminpassword"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
    assert "access_token" in data

# Test admin_resource endpoint
@pytest.mark.asyncio
async def test_admin_resource():
    async with httpx.AsyncClient() as client:
        # First, obtain an access token by logging in
        login_response = await client.post(f"{base_url}/token", json={"username": "admin", "password": "adminpassword"})
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Use the access token to access the admin_resource endpoint
        response = await client.get(f"{base_url}/admin", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == True
        assert "services" in data

# Test user_resource endpoint
@pytest.mark.asyncio
async def test_user_resource():
    async with httpx.AsyncClient() as client:
        # First, obtain an access token by logging in
        login_response = await client.post(f"{base_url}/token", json={"username": "user", "password": "userpassword"})
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Use the access token to access the user_resource endpoint
        response = await client.get(f"{base_url}/user", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"]  == True
        assert "services" in data
