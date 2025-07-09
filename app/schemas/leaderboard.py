from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    username: str
    total_games: int
    average_deviation: float
    best_deviation: float
