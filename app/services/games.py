from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.db import models
from app.db.models import GameSession, SessionStatus


TARGET_TIME_MS = 10_000
SESSION_EXPIRATION_MINUTES = 30

# Para asegurarme que el datetime es aware y no
def ensure_aware(dt: datetime) -> datetime:
    """
    Ensure a datetime is timezone-aware in UTC.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


async def start_game_session(user_id: int, db: AsyncSession) -> models.GameSession:
    """
    Starts a new game session for the given user.
    """
    now = datetime.now(timezone.utc)
    session = models.GameSession(
        user_id=user_id,
        start_time=now,
        status=models.SessionStatus.STARTED,
        created_at=now,
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def stop_game_session(session_id: int, user_id: int, db) -> GameSession:
    """
    Stops a game session, calculates duration and deviation.
    """
    result = await db.execute(select(GameSession).where(GameSession.id == session_id))
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to stop this session"
        )
    if session.status != SessionStatus.STARTED:
        raise HTTPException(
            status_code=400, detail="Session already completed or expired"
        )

    start_time = ensure_aware(session.start_time)
    now = datetime.now(timezone.utc)

    if now - start_time > timedelta(minutes=SESSION_EXPIRATION_MINUTES):
        session.status = SessionStatus.EXPIRED
        await db.commit()
        raise HTTPException(status_code=400, detail="Session has expired")

    session.stop_time = now
    session.duration = (now - start_time).total_seconds() * 1000 #ms
    session.deviation = abs(session.duration - TARGET_TIME_MS)
    session.status = SessionStatus.COMPLETED

    await db.commit()
    await db.refresh(session)
    return session
