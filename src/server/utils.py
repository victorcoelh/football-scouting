from pathlib import Path
from typing import Any

import pandas as pd

from lib.model.player_model import PlayerData, PlayerSeason, PlayerPer90, PlayerPerGame


#TODO: Obter imagens dos jogadores via google
def get_player_image(player_id: int) -> Path:
    image_path = Path(f"data/images/{player_id}.png")
    image_path = Path("data/images/2.png") if not image_path.is_file() else image_path

    return image_path

def get_player_from_id(database: pd.DataFrame, player_id: int) -> PlayerData:
    player_seasons = database[database["id"] == player_id]
    base_data = player_seasons.iloc[0].to_dict()
    
    player_seasons = [PlayerSeason.model_validate(season.to_dict())
                      for _, season in player_seasons.iterrows()]
    base_data["seasons"] = player_seasons

    return PlayerData.model_validate(base_data)

def get_criteria() -> list[str]:
    attributes = set(PlayerSeason.model_fields.keys()).union(
        list(PlayerPerGame.model_fields.keys()),
        list(PlayerPer90.model_fields.keys()))
    
    attributes.remove("per_90")
    attributes.remove("per_game")
    return list(attributes)

def flatten_nested_dict(nested: dict[str, Any]) -> dict[str, Any]:
    stack = list(nested.items())
    ans = {}

    while stack:
        key, val = stack.pop()
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                stack.append((sub_key, sub_val))
        else:
            ans[key] = val
    return dict(reversed(list(ans.items())))

def find_substring_in_list(array: list[str], substring: str) -> int:
    return next(i for i, string in enumerate(array) if substring in string)
