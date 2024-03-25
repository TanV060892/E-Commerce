import pytest,httpx 

# Define test data and constants
base_url = "http://localhost:8000/api"
admin_credentials = {"username": "admin", "password": "adminpassword"}
user_credentials = {"username": "user", "password": "userpassword"}
sample_item = {"name": "Balaji Wafers", "quantity": 10, "price": 190.99}

@pytest.mark.asyncio
async def test_add_items():
    async with httpx.AsyncClient() as client:
        # Log in as an admin to obtain an access token
        access_token = await get_access_token(client, admin_credentials)

        # Use the access token to add a new item
        response = await add_item(client, sample_item, access_token)

        # Check the response
        assert response.status_code == 201
        data = response.json()
        assert data["status"] is True
        assert "message" in data

@pytest.mark.asyncio
async def test_view_items():
    async with httpx.AsyncClient() as client:
        # Log in as a user to obtain an access token
        access_token = await get_access_token(client, user_credentials)

        # Use the access token to view all added items
        response = await view_items(client, access_token)

        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] is True
        assert "items" in data

# Helper functions

async def get_access_token(client, credentials):
    login_response = await client.post(f"{base_url}/token", json=credentials)
    assert login_response.status_code == 200
    return login_response.json()["access_token"]

async def add_item(client, item_data, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    return await client.post(f"{base_url}/items", json=item_data, headers=headers)

async def view_items(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    return await client.get(f"{base_url}/items", headers=headers)