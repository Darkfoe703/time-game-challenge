import pytest
import secrets
from sqlalchemy import delete
from app.db.models import User


@pytest.mark.asyncio
async def test_register_login_success_and_cleanup(async_client, db_session):
    #  datos únicos
    suffix = secrets.token_hex(4)
    username = f"user_{suffix}"
    email = f"{username}@example.com"
    password = "securepass123"
    

    # Registroo
    register_response = await async_client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert (
        register_response.status_code == 201
    ), f"Register failed: {register_response.text}"

    # Login
    login_response = await async_client.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # limpiar el usuario manualmente
    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()
