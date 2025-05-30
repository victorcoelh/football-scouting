from nicegui import ui
import pandas as pd
from returns.maybe import Some, Nothing

from gui.state import AppState
from gui.update import go_to_player
from player_data.player_data import PlayerData
from utils import get_player_image


#TODO: Deixar as linhas da tabela clicáveis
#TODO: Adicionar um botão de voltar

@ui.refreshable
def main_window(state: AppState, query_response: pd.DataFrame):
    match state.current_player:
        case Some(player):
            player_screen(player, state.similar_players.unwrap())
        case Nothing:
            dashboard(state, query_response)
    
def dashboard(state: AppState, query_response: pd.DataFrame):
    autocomplete_options = query_response["name"].to_list()
    with ui.column().classes("w-full items-center"):
        textbox = ui.input(placeholder="Player Name", autocomplete=autocomplete_options)\
            .props("rounded outlined dense")
        textbox.on("keydown.enter", lambda _: (go_to_player(state, textbox.value),
                                               main_window.refresh()))

        players_table(query_response)
        
def players_table(query_response: pd.DataFrame):
    player_data: list[dict] = []
    for i, player in query_response.iterrows():
        player_data.append(player.to_dict())

    ui.table(rows= player_data)
    
def player_screen(player: PlayerData, similar_players: list[PlayerData]):   
    with ui.column().classes("w-full items-center"):
        player_widget(player)
        ui.separator()
        with ui.row(align_items="start"):
            stats_widget(player)
            related_widget(similar_players)

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
