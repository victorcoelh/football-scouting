from pydantic import TypeAdapter
import requests

from lib.model.player_model import PlayerData


def fetch_player_data(player_id: int) -> PlayerData:
    response = requests.get(f"http://127.0.0.1:8000/players/{player_id}")
    return PlayerData.model_validate(response.json())

def fetch_similar_players(player_id: int) -> list[PlayerData]:
    response = requests.get(f"http://127.0.0.1:8000/similar/{player_id}")
    adapter = TypeAdapter(list[PlayerData])
    return adapter.validate_python(response.json())

def fetch_player_by_name(player_name: str) -> PlayerData:
    response = requests.get(f"http://127.0.0.1:8000/players_by_name/{player_name}")
    return PlayerData.model_validate(response.json())

def fetch_players() -> list[PlayerData]:
    response = requests.get("http://127.0.0.1:8000/all_players/")
    adapter = TypeAdapter(list[PlayerData])
    return adapter.validate_python(response.json())

def fetch_query(filter: str, column_a: str, column_b: str) -> tuple[list[int], list[float], list[float]]:
    if not filter or not column_a or not column_b:
        return ([], [], [])
    
    response = requests.get(f"http://127.0.0.1:8000/query/?filter={filter}&column_a={column_a}&column_b={column_b}")
    print (response.json())
    return 0
