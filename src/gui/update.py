import pandas as pd
from player_data.player_data import PlayerData
from returns.maybe import Some

from gui.state import AppState
from player_data.data_loading import load_data
from player_data.data_transform import most_similar_players


def fetch_player_data():
    pass

def get_player_id(database: pd.DataFrame, player_name: str) -> int:

    player_id = database["name"].to_list().index(player_name)
    return player_id

def go_to_player(state: AppState, player_name: str) -> None:
    database = load_data()
    player_id = get_player_id(database, player_name)
    current_player = PlayerData(database, player_id)
    
    state.current_player = Some(current_player)
    similar_players = most_similar_players(
        database,
        player_id,
        ["goals", "assists", "height", "value", "age"]
    )
    
    similar_players = list(map(lambda x: PlayerData(database, x), similar_players))
    state.similar_players = Some(similar_players)
