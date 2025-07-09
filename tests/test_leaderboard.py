import pytest


@pytest.mark.asyncio
async def test_get_leaderboard(async_client):
    response = await async_client.get("/leaderboard")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
