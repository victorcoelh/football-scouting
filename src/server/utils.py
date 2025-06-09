from pathlib import Path

import pandas as pd

from lib.model.player_data import PlayerData


def get_player_image(player_id: int) -> Path:
    return Path(f"data/images/{player_id}.png")

def get_player_from_id(database: pd.DataFrame, player_id: int) -> PlayerData:
    player_row = database.iloc[player_id].to_dict()
    player_row["id"] = player_id
    return PlayerData.model_validate(player_row)
