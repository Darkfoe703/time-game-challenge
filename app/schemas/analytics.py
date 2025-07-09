from pydantic import BaseModel
from datetime import datetime
from typing import List


class GameSummary(BaseModel):
    id: int
    start_time: datetime
    stop_time: datetime
    duration: float
    deviation: float

    class Config:
        model_config = {"from_attributes": True}


class UserAnalytics(BaseModel):
    username: str
    total_games: int
    average_deviation: float
    best_deviation: float
    game_history: List[GameSummary]
