from pydantic import TypeAdapter
from returns.maybe import Some, Nothing
import requests

from web_client.gui.state import AppState
from lib.model.player_data import PlayerData


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
    response = requests.get("http://127.0.0.1:8000/query/")
    adapter = TypeAdapter(list[PlayerData])
    return adapter.validate_python(response.json())

def go_to_dashboard(state: AppState) -> None:
    state.current_player = Nothing
    state.similar_players = Nothing

def go_to_player(state: AppState, player_id: int) -> None:
    player = fetch_player_data(player_id)
    state.current_player = Some(player)

    similar_players = fetch_similar_players(player_id)
    state.similar_players = Some(similar_players)
    
def go_to_player_named(state: AppState, player_name: str) -> None:
    player = fetch_player_by_name(player_name)
    state.current_player = Some(player)

    similar_players = fetch_similar_players(player.id)
    state.similar_players = Some(similar_players)
