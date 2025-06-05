from returns.maybe import Some
import requests

from web_client.gui.state import AppState
from lib.player_data import PlayerData


def fetch_player_data(player_id: int) -> PlayerData:
    response = requests.get(f"http://127.0.0.1:8000/players/{player_id}")
    return PlayerData.model_validate(response.json())

def fetch_similar_players(player_id: int) -> list[PlayerData]:
    return []

def go_to_player(state: AppState, player_id: int) -> None:
    player = fetch_player_data(player_id)
    state.current_player = Some(player)

    similar_players = fetch_similar_players(player_id)
    state.similar_players = Some(similar_players)
