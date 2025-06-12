from typing import Any
from pydantic import BaseModel, model_validator

   
class PlayerPer90(BaseModel):
    goals_per_90: float
    assists_per_90: float
    cards_per_90: float
    passes_per_90: float
    dribbles_per_90: float
    key_passes_per_90: float
    fouls_drawn_per_90: float
    blocks_per_90: float
    saves_per_90: float
    crosses_per_90: float
    distance_travelled_per_90: float


class PlayerRates(BaseModel):
    pass_completion_rate: float
    dribbles_successful_percentage: float
    shot_conversion_rate: float
    save_percentage: float
    cross_completion_rate: float


class PlayerSeason(BaseModel):
    season: int
    appearances: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    average_rating: float
    per_90: PlayerPer90
    rates: PlayerRates
    
    @model_validator(mode="before")
    def unflatten_dict(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "per_90" in data.keys():
            return data
        
        player_per_90 = PlayerPer90.model_validate(data)
        player_rates = PlayerRates.model_validate(data)
        
        data["per_90"] = player_per_90
        data["rates"] = player_rates
        return data

    
class PlayerData(BaseModel):
    id: int
    name: str
    age: int
    position: str
    nationality: str
    club: str
    league: str
    salary: float
    market_value: float
    seasons: list[PlayerSeason]        
