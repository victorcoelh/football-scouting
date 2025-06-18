from typing import Any
from pydantic import BaseModel, model_validator


class PlayerPer90(BaseModel):
    goals_per_90: float
    assists_per_90: float
    crosses_per_90: float
    passes_per_90: float
    key_passes_per_90: float
    dribbles_per_90: float
    fouls_drawn_per_90: float
    cards_per_90: float
    blocks_per_90: float
    dispossesed_per_90: float
    fouls_committed_per_90: float
    saves_per_90: float


class PlayerPerGame(BaseModel):
    shots_on_target_per_game: float
    key_passes_per_game: float
    accurate_crosses_per_game: float
    dribbles_per_game: float
    fouls_drawn_per_game: float
    aerial_duels_won_per_game: float
    fouls_committed_per_game: float
    dispossesed_per_game: float
    blocks_per_game: float
    interceptions_per_game: float
    saves_per_game: float


class PlayerSeason(BaseModel):
    season: int
    appearances: int
    minutes_played: int
    average_rating: float
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    shot_conversion_rate: float
    pass_completion_rate: float
    cross_completion_rate: float
    dribbles_successful_percentage: float
    save_percentage: float
    per_90: PlayerPer90
    per_game: PlayerPerGame
    
    @model_validator(mode="before")
    def unflatten_dict(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "per_90" in data.keys():
            return data
        
        player_per_90 = PlayerPer90.model_validate(data)
        player_rates = PlayerPerGame.model_validate(data)
        
        data["per_90"] = player_per_90
        data["per_game"] = player_rates
        return data

    
class PlayerData(BaseModel):
    id: int
    name: str
    age: int
    position: str
    nationality: str
    club: str
    league: str
    seasons: list[PlayerSeason]        
