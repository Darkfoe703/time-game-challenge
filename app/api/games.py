from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.api.deps import get_current_user, get_db
from app.schemas.game import GameSessionOut
from app.services.games import start_game_session, stop_game_session

router = APIRouter(prefix="/games", tags=["Game"])


@router.post(
    "/start", response_model=GameSessionOut, status_code=status.HTTP_201_CREATED
)
async def start_session(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Starts a new game session for the current user.
    """
    session = await start_game_session(current_user.id, db)
    return session


@router.post("/{session_id}/stop", response_model=GameSessionOut)
async def stop_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Stops a game session and calculates deviation.
    """
    session = await stop_game_session(session_id, current_user.id, db)
    return session
