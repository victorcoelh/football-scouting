from nicegui import ui

from lib.model.player_model import PlayerData
from web_client.gui.controller.update import go_to_player
from web_client.gui.controller.networking import fetch_players
from web_client.gui.state.state import AppState


def dashboard(state: AppState):
    query_result = fetch_players()
    
    with ui.column(align_items="center").classes("full-width full-height justify-center p-20"):
        players_table(state, query_result)
        
def players_table(state: AppState, query_response: list[PlayerData]):
    player_dicts = [player.model_dump() for player in query_response]
    
    for ass in player_dicts:
        del ass["seasons"]

    table = ui.table(
        rows=player_dicts,
        row_key="id",
        pagination=15,
    ).classes("full-height full-width")\
    .props("virtual-scroll")\
    .style("border-radius: 10px;")
    
    table.on("rowClick", lambda event: go_to_player(state, event.args[2]))
