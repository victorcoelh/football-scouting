from dataclasses import dataclass
from typing import Literal

from returns.maybe import Maybe

from lib.model.player_model import PlayerData

@dataclass
class AppState:
    current_player: Maybe[PlayerData]
    similar_players: Maybe[list[PlayerData]]
    table_type: Literal["overall", "per_90", "rates"]
