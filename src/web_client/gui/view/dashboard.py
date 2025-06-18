from nicegui import ui

from lib.model.player_model import PlayerData
from web_client.gui.controller.update import go_to_player, go_to_player_named
from web_client.gui.controller.networking import fetch_players
from web_client.gui.state.state import AppState


def dashboard(state: AppState):
    query_result = fetch_players()
    autocomplete = [player.name for player in query_result]

    with ui.column().classes("w-full items-center"):
        textbox = ui.input(placeholder="Player Name", autocomplete=autocomplete)\
            .props("rounded outlined dense")
        textbox.on("keydown.enter", lambda _: go_to_player_named(state, textbox.value))

        players_table(state, query_result)
        
def players_table(state: AppState, query_response: list[PlayerData]):
    player_dicts = [player.model_dump() for player in query_response]
    
    for ass in player_dicts:
        del ass["seasons"]

    table = ui.table(
        rows=player_dicts,
        row_key="id",
        selection="single",
        pagination=15,
    ).classes("h-[750px]")\
    .props("virtual-scroll")\
    
    table.on("rowClick", lambda event: go_to_player(state, event.args[2]))
