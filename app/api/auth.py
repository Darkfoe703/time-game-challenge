from fastapi import APIRouter, Form, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import LoginRequest, Token
from app.db.database import AsyncSessionLocal
from app.services.auth import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    user = await create_user(user_in, db)
    return user


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await authenticate_user(login_data.email, login_data.password, db)
    return {"access_token": token, "token_type": "bearer"}
