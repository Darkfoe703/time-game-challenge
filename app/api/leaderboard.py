from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.schemas.leaderboard import LeaderboardEntry
from app.services.leaderboard import get_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=List[LeaderboardEntry])
async def leaderboard(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await get_leaderboard(page=page, size=size, db=db)
