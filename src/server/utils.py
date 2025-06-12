from pathlib import Path

import pandas as pd

from lib.model.player_model import PlayerData, PlayerSeason


def get_player_image(player_id: int) -> Path:
    return Path(f"data/images/{player_id}.png")

def get_player_from_id(database: pd.DataFrame, player_id: int) -> PlayerData:
    player_seasons = database[database["id"] == player_id]
    base_data = player_seasons.iloc[0].to_dict()
    
    player_seasons = [PlayerSeason.model_validate(season.to_dict())
                      for _, season in player_seasons.iterrows()]
    base_data["seasons"] = player_seasons

    return PlayerData.model_validate(base_data)
