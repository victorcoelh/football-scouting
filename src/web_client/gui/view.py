from nicegui import ui
from returns.maybe import Some, Nothing

from web_client.gui.state import AppState
from web_client.gui.update import go_to_player, fetch_players, go_to_player_named, go_to_dashboard
from lib.model.player_model import PlayerData
from server.utils import get_player_image


#TODO: Refatorar
#TODO: Adicionar um botão de voltar
#TODO: Obter imagens dos jogadores

@ui.refreshable
def main_window(state: AppState):
    match state.current_player:
        case Some(player):
            player_screen(state)
        case Nothing:
            dashboard(state)
    
def dashboard(state: AppState):
    query_result = fetch_players()
    autocomplete = [player.name for player in query_result]

    with ui.column().classes("w-full items-center"):
        textbox = ui.input(placeholder="Player Name", autocomplete=autocomplete)\
            .props("rounded outlined dense")
        textbox.on("keydown.enter", lambda _: (go_to_player_named(state, textbox.value),
                                               main_window.refresh()))

        players_table(state, query_result)
        
def players_table(state: AppState, query_response: list[PlayerData]):
    player_dicts = [player.model_dump() for player in query_response]
    
    for ass in player_dicts:
        del ass["seasons"]

    table = ui.table(
        rows=player_dicts,
        row_key="id",
        selection="single",
        on_select=lambda x: print("penisssss"),
        pagination=15,
    ).classes("h-[750px]")\
    .props("virtual-scroll")\
    
    table.on("rowClick", lambda event: (go_to_player(state, event.args[2]),
                                        main_window.refresh()))
    
def player_screen(state: AppState):
    player = state.current_player.unwrap()
     
    with ui.column().classes("w-full items-center"):
        player_widget(player)
        ui.separator()
        with ui.row(align_items="start"):
            with ui.column():
                toggle_widget(state)
                stats_widget(state, player)
            related_widget(state, state.similar_players.unwrap())
            
    ui.on("keydown.escape", lambda _: (go_to_dashboard(state),
                                       main_window.refresh()))

def player_widget(player: PlayerData):
    with ui.row(wrap=False, align_items="end").classes():
        ui.image(get_player_image(player.id)).classes("w-32")
        with ui.column(align_items="start"):
            ui.label(player.name)
            with ui.row(wrap=False):
                ui.label(player.club)
                ui.label(f"{player.age}y")
                ui.label(f"{player.nationality}")
                
def toggle_widget(state: AppState):
    ui.toggle(["overall", "per_90", "rates"], on_change=stats_widget.refresh)\
      .bind_value(state, "table_type")

@ui.refreshable
def stats_widget(state: AppState, player: PlayerData):
    player_dicts = [season.model_dump() for season in player.seasons]

    if state.table_type != "overall":
        player_dicts = [season[state.table_type] for season in player_dicts] # type: ignore
    else:
        for season in player_dicts:
            del season["per_90"]
            del season["rates"]

    ui.table(rows=player_dicts)\
        .classes("w-[1200px]")\
        .props("virtual-scroll")\

def related_widget(state: AppState, similar_players: list[PlayerData]):
    with ui.column():
        with ui.card():
            ui.label("SIMILAR PLAYERS")
        for player in similar_players[:3]:
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
        card.on("click", lambda player_id: (go_to_player(state, player.id),
                                            main_window.refresh()))
