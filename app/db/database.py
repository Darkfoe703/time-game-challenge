from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy asyncengine !!!!
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()
