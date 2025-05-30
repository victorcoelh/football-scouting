import pandas as pd

from dataclasses import dataclass


@dataclass
class PlayerData:
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
    
    def __init__(self, database: pd.DataFrame, player_id: int):
        self.id = player_id
        player_row = database.iloc[player_id]
        
        for column, value in player_row.items():
            self.__setattr__(column, value) # type: ignore
    