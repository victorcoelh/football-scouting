from typing import Hashable
from urllib.parse import unquote

import pandas as pd
from fastapi import FastAPI

from server.load_database import load_data, normalize_data
from server.services import most_similar_players
from lib.model.player_model import PlayerData
from server.utils import get_criteria, get_player_from_id, find_substring_in_list

app = FastAPI()
database = load_data("./data/jogadores_brasil_no_bad_columns.csv")
normalized_data = normalize_data(database)


@app.get("/players/{player_id}")
async def get_player_data(player_id: int) -> PlayerData:
    return get_player_from_id(database, player_id)

@app.get("/players_by_name/{player_name}")
async def get_player_by_name(player_name: str) -> PlayerData:
    player_name = unquote(player_name)
    id_match = find_substring_in_list(database["name"].to_list(), player_name)
    
    return get_player_from_id(database, id_match)

#TODO: Filter to position before comparisons
@app.get("/similar/{player_id}")
async def get_similar_players(player_id: int) -> list[PlayerData]:
    criteria = get_criteria()
    similar_players = most_similar_players(normalized_data, player_id, criteria)[:5]

    return list(map(
        lambda player_id: get_player_from_id(database, player_id),
        similar_players
     ))

@app.get("/query/")
async def get_query() -> list[PlayerData]:
    top_results = database["id"].to_list()

    return [get_player_from_id(database, player_id)
            for player_id in top_results]

def row_tuple_to_player_data(row_tuple: tuple[Hashable, pd.Series]) -> PlayerData:
    row_dict = row_tuple[1].to_dict()
    row_dict["id"] = row_tuple[0]
    return PlayerData.model_validate(row_dict)
