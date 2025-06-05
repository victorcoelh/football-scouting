from fastapi import FastAPI

from server.load_database import load_data, normalize_data
from server.services import most_similar_players
from lib.player_data import PlayerData
from server.utils import get_player_from_id

app = FastAPI()
database = load_data("./data/mock_data.csv")
normalized_data = normalize_data(database)


@app.get("/players/{player_id}")
async def get_player_data(player_id: int) -> PlayerData:
    return get_player_from_id(database, player_id)

@app.get("/similar/{player_id}")
async def get_similar_players(player_id: int) -> list[PlayerData]:
    similar_players = most_similar_players(
        normalized_data,
        player_id,
        ["goals", "assists", "height", "rating"]
    )[:5]

    return list(map(lambda player_id: get_player_from_id(database, player_id), similar_players))

@app.get("/query/", status_code=404)
async def get_query(query_type: str, query_params: str) -> list[PlayerData]:
    raise NotImplementedError()
