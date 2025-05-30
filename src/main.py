from returns.maybe import Some, Nothing

from player_data.data_transform import most_similar_players
from player_data.player_data import PlayerData
from gui.state import AppState
from gui.view import main_window
from player_data.data_loading import load_data, normalize_data


if __name__ in {"__main__", "__mp_main__"}:
    player_id = 2
    
    database = load_data()
    normalized_data = normalize_data(database)

    first_player = PlayerData(database, player_id)
    similar_players = most_similar_players(normalized_data, player_id, ["goals", "assists", "height", "rating"])
    similar_players = list(map(lambda x: PlayerData(database, x), similar_players))
    state = AppState(Some(first_player), Some(similar_players))
    
    main_window(state)
