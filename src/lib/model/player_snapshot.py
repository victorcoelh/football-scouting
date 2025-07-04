from pydantic import BaseModel


class PlayerSnapshot(BaseModel):
    id: int
    name: str
    stats: dict[str, float]
