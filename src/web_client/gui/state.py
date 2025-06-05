from dataclasses import dataclass

from returns.maybe import Maybe

from lib.player_data import PlayerData

@dataclass
class AppState:
    current_player: Maybe[PlayerData]
    similar_players: Maybe[list[PlayerData]]
