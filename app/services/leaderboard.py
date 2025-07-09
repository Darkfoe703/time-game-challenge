from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, GameSession, SessionStatus


async def get_leaderboard(page: int, size: int, db: AsyncSession):
    """
    Returns a paginated leaderboard ordered by average deviation.
    """
    offset = (page - 1) * size

    # Subquery: aggregate stats per user
    stats_subq = (
        select(
            GameSession.user_id.label("user_id"),
            func.count().label("total_games"),
            func.avg(GameSession.deviation).label("average_deviation"),
            func.min(GameSession.deviation).label("best_deviation"),
        )
        .where(GameSession.status == SessionStatus.COMPLETED)
        .group_by(GameSession.user_id)
        .subquery()
    )

    # Aliases (optional, helps with clarity)
    stats_alias = aliased(stats_subq)

    # Join wiht User to get username
    query = (
        select(
            User.username,
            stats_alias.c.total_games,
            stats_alias.c.average_deviation,
            stats_alias.c.best_deviation,
        )
        .join(stats_alias, User.id == stats_alias.c.user_id)
        .order_by(stats_alias.c.average_deviation.asc())
        .offset(offset)
        .limit(size)
    )

    result = await db.execute(query)
    return result.all()
