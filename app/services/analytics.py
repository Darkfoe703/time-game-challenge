from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, GameSession, SessionStatus
from fastapi import HTTPException


async def get_user_analytics(user_id: int, db: AsyncSession):
    # Get user
    user_stmt = select(User).where(User.id == user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Aggregate stats
    stats_stmt = (
        select(
            func.count(GameSession.id),
            func.avg(GameSession.deviation),
            func.min(GameSession.deviation),
        )
        .where(GameSession.user_id == user_id)
        .where(GameSession.status == SessionStatus.COMPLETED)
    )
    stats_result = await db.execute(stats_stmt)
    total_games, average_deviation, best_deviation = stats_result.one()

    # Game history
    history_stmt = (
        select(GameSession)
        .where(GameSession.user_id == user_id)
        .where(GameSession.status == SessionStatus.COMPLETED)
        .order_by(GameSession.start_time.desc())
    )
    history_result = await db.execute(history_stmt)
    history = history_result.scalars().all()

    return {
        "username": user.username,
        "total_games": total_games or 0,
        "average_deviation": average_deviation or 0.0,
        "best_deviation": best_deviation or 0.0,
        "game_history": history,
    }
