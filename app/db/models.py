from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum

from app.db.database import Base


class SessionStatus(PyEnum):
    STARTED = "started"
    COMPLETED = "completed"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # one to many relationship one user ha many game sessions.
    game_sessions = relationship("GameSession", back_populates="user")


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    stop_time = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Float, nullable=True)  # milliseconds
    deviation = Column(Float, nullable=True)  #from 10000 ms
    status = Column(Enum(SessionStatus), default=SessionStatus.STARTED)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Many toone relationship session belongs to one user
    user = relationship("User", back_populates="game_sessions")
