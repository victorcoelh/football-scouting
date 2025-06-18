from web_client.gui.controller.networking import fetch_player_by_name, fetch_player_data
from web_client.gui.state.state import AppState


def go_to_dashboard(state: AppState) -> None:
    state.current_player = None

def go_to_player(state: AppState, player_id: int) -> None:
    player = fetch_player_data(player_id)
    state.current_player = player
    
def go_to_player_named(state: AppState, player_name: str) -> None:
    player = fetch_player_by_name(player_name)
    state.current_player = player
