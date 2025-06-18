from nicegui import ui

from lib.model.player_model import PlayerData
from server.utils import get_player_image
from web_client.gui.controller.update import go_to_dashboard, go_to_player
from web_client.gui.state.state import AppState


#TODO: Adicionar um botão de voltar
#TODO: Obter imagens dos jogadores
def player_screen(state: AppState):
    if state.current_player is None:
        raise ValueError("No player selected.")
    
    with ui.column().classes("w-full items-center"):
        player_widget(state.current_player)
        ui.separator()
        with ui.row(align_items="start"):
            with ui.column():
                toggle_widget(state)
                stats_widget(state)
                state.subscribe(stats_widget.refresh, "table_type")
            related_widget(state)
            
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

    ui.table(rows=player_dicts)\
        .classes("w-[1200px]")\
        .props("virtual-scroll")\

def related_widget(state: AppState):
    with ui.column():
        with ui.card():
            ui.label("SIMILAR PLAYERS")
        for player in state.similar_players[:5]: # type: ignore
            similar_player_card(state, player)

#TODO: Filter showed stats on similar player to most relevant stats
def similar_player_card(state: AppState, player: PlayerData):  
    with ui.card() as card:
        with ui.column():
            ui.label(player.name)
            with ui.row():
                ui.label(f"G: {player.seasons[0].goals}")
                ui.label(f"A: {player.seasons[0].assists}")
                ui.label(f"R: {player.seasons[0].average_rating}")
        card.on("click", lambda player_id: go_to_player(state, player.id))
