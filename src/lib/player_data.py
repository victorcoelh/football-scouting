from pydantic import BaseModel


class PlayerData(BaseModel):
    id: int
    name: str
    age: int
    height: int
    team: str
    position: str
    value: float
    goals: int
    assists: int
    rating: float
