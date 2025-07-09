import pytest
from tests.helpers import create_test_user, delete_test_user


@pytest.mark.asyncio
async def test_start_and_stop_game_session(async_client, db_session):
    # Crear usuario y token
    user_data = await create_test_user(async_client, db_session)
    headers = {"Authorization": f"Bearer {user_data['token']}"}

    # Iniciar sesión de juego
    start_response = await async_client.post("/games/start", headers=headers)
    assert start_response.status_code == 201
    session_id = start_response.json()["id"]

    # Detener sesión de juego
    stop_response = await async_client.post(
        f"/games/{session_id}/stop", headers=headers
    )
    assert stop_response.status_code == 200
    stop_data = stop_response.json()
    assert stop_data["status"] == "completed"

    # Eliminar usuario de prueba
    await delete_test_user(user_data["email"], db_session)
