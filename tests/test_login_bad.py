import pytest


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client):
    response = await async_client.post(
        "/auth/login",
        json={"email": "fakeuser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()
