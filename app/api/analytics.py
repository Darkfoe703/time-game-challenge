from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.analytics import UserAnalytics
from app.services.analytics import get_user_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/user/{user_id}", response_model=UserAnalytics)
async def user_analytics(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_analytics(user_id, db)
