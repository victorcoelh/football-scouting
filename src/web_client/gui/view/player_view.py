from nicegui import ui

from lib.model.player_model import PlayerData
from server.utils import get_player_image
from web_client.gui.controller.update import go_to_dashboard, go_to_player
from web_client.gui.state.state import AppState


def player_screen(state: AppState):
    if state.current_player is None:
        raise ValueError("No player selected.")

    with ui.column().classes("full-width full-height p-20"):
        player_widget(state.current_player)
        ui.separator()

        with ui.row(align_items="start", wrap=False).classes("full-width justify-between items-start"):
            stats_widget(state)
            related_widget(state)
            state.subscribe(stats_widget.refresh, "table_type")

        graphics_widget()

    ui.on("keydown.escape", lambda _: go_to_dashboard(state))

def player_widget(player: PlayerData):
    with ui.row(wrap=False, align_items="end").classes():
        ui.image(get_player_image(player.id)).classes("w-32")
        with ui.column(align_items="start"):
            ui.label(player.name)
            with ui.row(wrap=False):
                ui.label(player.position)
                ui.label(player.club)
                ui.label(f"{player.age}y")
                ui.label(f"{player.nationality}")
                
def toggle_widget(state: AppState):
    ui.toggle(["overall", "per_game", "per_90"])\
      .bind_value(state, "table_type")

@ui.refreshable
def stats_widget(state: AppState):
    player_dicts = [season.model_dump()
                    for season in state.current_player.seasons] # type: ignore

    if state.table_type != "overall":
        player_dicts = [season[state.table_type] for season in player_dicts] # type: ignore
    else:
        for season in player_dicts:
            del season["per_90"]
            del season["per_game"]
            
    with ui.column(align_items="start").classes("w-4/5"):
        toggle_widget(state)
        ui.table(rows=player_dicts)\
            .classes("full-width")\
            .props("virtual-scroll")\

def related_widget(state: AppState):
    with ui.column(align_items="start").classes("items-start"):
        for player in state.similar_players[:5]: # type: ignore
            similar_player_card(state, player)

#TODO: Filter showed stats on similar player to most relevant stats
def similar_player_card(state: AppState, player: PlayerData):  
    with ui.card().classes("w-[355px]").style("background-color: #272C3B") as card:
        with ui.column():
            ui.label(player.name)
            with ui.row():
                ui.label(f"Goals: {player.seasons[0].goals}")
                ui.label(f"Assists: {player.seasons[0].assists}")
                ui.label(f"Rating: {player.seasons[0].average_rating}")
        card.on("click", lambda player_id: go_to_player(state, player.id))
        
def graphics_widget():
    ui.label("Graphics")
