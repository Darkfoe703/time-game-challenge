from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.db import models
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token


async def create_user(user_in: UserCreate, db: AsyncSession) -> models.User:
    """
    Creates a new user in the database after hashing the password.
    """
    # check if user already exists
    result = await db.execute(
        select(models.User).where(models.User.email == user_in.email)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash the password and create the user
    hashed_pw = hash_password(user_in.password)
    user = models.User(
        username=user_in.username, email=user_in.email, hashed_password=hashed_pw
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(email: str, password: str, db: AsyncSession) -> str:
    """
    Verifies user credentials and returns a JWT token if valid.
    """
    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": user.username})
    return token
