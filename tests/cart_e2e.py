import pytest,httpx

# Define the base URL of your FastAPI application
base_url = "http://localhost:8000/api"

# Sample user credentials for testing
user_credentials = {
    "username": "user",
    "password": "userpassword",
}

# Sample item code and quantity for testing
sample_item_code = 9
sample_item_quantity = 3

@pytest.mark.asyncio
async def test_add_items_to_cart():
    async with httpx.AsyncClient() as client:
        # First, obtain an access token by logging in
        login_response = await client.post(f"{base_url}/token", json=user_credentials)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Use the access token to add items to the cart
        response = await client.post(
            f"{base_url}/cart",
            json={"code": sample_item_code, "quantity": sample_item_quantity},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        
        # Check the response
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == True
        assert "message" in data

@pytest.mark.asyncio
async def test_remove_item_from_cart():
    async with httpx.AsyncClient() as client:
        # First, obtain an access token by logging in
        login_response = await client.post(f"{base_url}/token", json=user_credentials)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Use the access token to remove an item from the cart
        response = await client.delete(
            f"{base_url}/cart/{sample_item_code}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == True
        assert "message" in data