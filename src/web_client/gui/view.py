from nicegui import ui
from returns.maybe import Some, Nothing

from web_client.gui.state import AppState
from web_client.gui.update import go_to_player, fetch_players, go_to_player_named, go_to_dashboard
from lib.model.player_data import PlayerData
from server.utils import get_player_image


#TODO: Deixar os outros jogadores clicáveis
#TODO: Adicionar um botão de voltar

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

    table = ui.table(
        rows=player_dicts,
        row_key="id",
        selection="single",
        on_select=lambda x: print("penisssss")
    )
    
    table.on("rowClick", lambda event: (go_to_player(state, event.args[2]),
                                        main_window.refresh()))
    
def player_screen(state: AppState):
    player = state.current_player.unwrap()
     
    with ui.column().classes("w-full items-center"):
        player_widget(player)
        ui.separator()
        with ui.row(align_items="start"):
            stats_widget(player)
            related_widget(state.similar_players.unwrap())
            
    ui.on("keydown.escape", lambda _: (go_to_dashboard(state),
                                       main_window.refresh()))

def player_widget(player: PlayerData):
    with ui.row(wrap=False, align_items="end").classes():
        ui.image(get_player_image(player.id)).classes("w-32")
        with ui.column(align_items="start"):
            ui.label(player.name)
            with ui.row(wrap=False):
                ui.label(player.team)
                ui.label(f"€{player.value}M")
                ui.label(f"{player.age}y")
                ui.label(f"{player.height}cm")

def stats_widget(player: PlayerData):
    example_row = {"year": "24-25", "goals": player.goals, "assists": player.assists, "rating": player.rating}
    
    ui.table(rows=[
        example_row,
        example_row,
        example_row
    ], columns=[
        {"name": "year", "label": "SEASON", "field": "year"},
        {"name": "goals", "label": "GOALS", "field": "goals"},
        {"name": "assists", "label": "ASSISTS", "field": "assists"},
        {"name": "rating", "label": "RATING", "field": "rating"},
    ], column_defaults={
        'align': 'left',
        'headerClasses': 'uppercase text-primary',
    })

def related_widget(similar_players: list[PlayerData]):
    with ui.column():
        with ui.card():
            ui.label("SIMILAR PLAYERS")
        for player in similar_players[:3]:
            similar_player_card(player)

#TODO: Filter showed stats on similar player to most relevant stats
def similar_player_card(player: PlayerData):
    with ui.card():
        with ui.column():
            ui.label(player.name)
            with ui.row():
                ui.label(f"G: {player.goals}")
                ui.label(f"A: {player.assists}")
                ui.label(f"R: {player.rating}")
