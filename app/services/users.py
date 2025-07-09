from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models


async def get_user_by_username(username: str, db: AsyncSession) -> models.User | None:
    result = await db.execute(
        select(models.User).where(models.User.username == username)
    )
    return result.scalars().first()
