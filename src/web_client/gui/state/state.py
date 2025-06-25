from typing import Callable, Literal

from lib.model.player_model import PlayerData
from web_client.gui.controller.networking import fetch_similar_players

type SubscriberFn = Callable[[AppState], None]
type TableType = Literal["overall", "per_game", "per_90"]


class AppState:
    __subscribers: dict[str, list[SubscriberFn]]
    _current_player: PlayerData | None
    _similar_players: list[PlayerData] | None
    _graphic_filter: str
    _graphic_column_a: str
    _graphic_column_b: str
    _table_type: TableType
    
    def __init__(self) -> None:
        self._current_player = None
        self._similar_players = None
        self._table_type = "overall"
        
        self.__subscribers = {
            "current_player": [],
            "similar_players": [],
            "table_type": [],
            "graphic_filter": [],
            "graphic_column_a": [],
            "graphic_column_b": [],
        }
        
    @property
    def current_player(self) -> PlayerData | None:
        return self._current_player
    
    @property
    def similar_players(self) -> list[PlayerData] | None:
        return self._similar_players
    
    @property
    def table_type(self) -> TableType:
        return self._table_type
    
    @property
    def graphic_filter(self) -> str:
        return self._graphic_filter
    
    @property
    def graphic_column_a(self) -> str:
        return self._graphic_column_a

    @property
    def graphic_column_b(self) -> str:
        return self._graphic_column_b
    
    @graphic_filter.setter
    def graphic_filter(self, value: str) -> None:
        self._graphic_filter = value
        
        for callback in self.__subscribers["graphic_filter"]:
            callback(self)
    
    @graphic_column_a.setter
    def graphic_column_a(self, value: str) -> None:
        self._graphic_column_a = value
        
        for callback in self.__subscribers["graphic_column_a"]:
            callback(self)
    
    @graphic_column_b.setter
    def graphic_column_b(self, value: str) -> None:
        self._graphic_column_b = value
        
        for callback in self.__subscribers["graphic_column_b"]:
            callback(self)
    
    @current_player.setter
    def current_player(self, value: PlayerData | None) -> None:
        if value is not None:
            self._similar_players = fetch_similar_players(value.id)
        else:
            self._similar_players = None

        self._current_player = value
        for callback in self.__subscribers["current_player"]:
            callback(self)
            
    @table_type.setter
    def table_type(self, value: TableType) -> None:
        self._table_type = value
        
        for callback in self.__subscribers["table_type"]:
            callback(self)
    
    def subscribe(self, callback: SubscriberFn, attribute: str) -> None:
        self.__subscribers[attribute].append(callback)
