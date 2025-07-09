from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.database import AsyncSessionLocal
from app.services.users import get_user_by_username
from app.db.models import User

bearer_scheme = HTTPBearer()

#Get DB session dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


#Dependency to get current authenticated user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    username = decode_access_token(token)
    user = await get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
