import pytest
import secrets
from sqlalchemy import delete
from app.db.models import User

@pytest.mark.asyncio
async def test_auth_register_and_login_errors(async_client, db_session):
    suffix = secrets.token_hex(4)
    email = f"user_{suffix}@example.com"
    password = "securepass123"
    username = f"user_{suffix}"

    #registro inicial
    await async_client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    #  Registro duplicado
    duplicate_response = await async_client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert (
        duplicate_response.status_code == 400 or duplicate_response.status_code == 409
    )

    # Login con email incorrecto
    bad_email_response = await async_client.post(
        "/auth/login", json={"email": "nonexistent@example.com", "password": password}
    )
    assert bad_email_response.status_code == 401

    # Login con password incorrecta
    bad_password_response = await async_client.post(
        "/auth/login", json={"email": email, "password": "wrongpassword"}
    )
    assert bad_password_response.status_code == 401

    # limpieza de losd atos de prueba
    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()
