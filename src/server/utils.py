from typing import Any

import pandas as pd

from lib.model.player_model import PlayerData, PlayerSeason, PlayerPer90, PlayerPerGame
from lib.model.player_snapshot import PlayerSnapshot


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

def series_to_snapshot(player_id: int, player: pd.Series, column_a: str, column_b: str) -> PlayerSnapshot:
    return PlayerSnapshot(
        id=player_id, # type: ignore
        name=player["name"],
        stats={
            column_a: player[column_a],
            column_b: player[column_b]
        }
    )

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
