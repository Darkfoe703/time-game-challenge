import secrets
from sqlalchemy import delete
from app.db.models import User


async def create_test_user(async_client, db_session, password="securepass123"):
    """
    Registra un usuario aleatorio y devuelve un dict con username, email, password y token.
    """
    suffix = secrets.token_hex(4)
    username = f"user_{suffix}"
    email = f"{username}@example.com"

    # Rregistrar usuario
    await async_client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    # Login y obtener token
    login_res = await async_client.post(
        "/auth/login", json={"email": email, "password": password}
    )

    token = login_res.json()["access_token"]

    return {"username": username, "email": email, "password": password, "token": token}


async def delete_test_user(email, db_session):
    """
    Elimina un usuario por su email.
    """
    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()
