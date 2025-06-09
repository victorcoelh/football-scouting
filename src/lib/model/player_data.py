from pydantic import BaseModel

    
class PlayerBio(BaseModel):
    name: str
    age: int
    position: str
    nationality: str
    

class PlayerCareer(BaseModel):
    club: str
    league: str
    salary: float
    market_value: float

    
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
    appearences: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    average_rating: float
    per_90: PlayerPer90

    
class PlayerData(BaseModel):
    id: int
    bio: PlayerBio
    career: PlayerCareer
    season: PlayerSeason
