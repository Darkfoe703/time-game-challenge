from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class SessionStatus(str, Enum):
    started = "started"
    completed = "completed"
    expired = "expired"


class GameSessionStart(BaseModel):
    # No input fields needed to start.
    pass


class GameSessionStop(BaseModel):
    # no fields needed to stop(session_id va en la ruta)
    pass


class GameSessionOut(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    stop_time: Optional[datetime] = None
    duration: Optional[float] = None
    deviation: Optional[float] = None
    status: SessionStatus

    class Config:
        model_config = {"from_attributes": True}
