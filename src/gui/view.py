from nicegui import ui

from gui.state import AppState
from player_data.player_data import PlayerData
from utils import get_player_image


def main_window(state: AppState):
    with ui.column().classes("w-full items-center"):
        player_widget(state.current_player.unwrap())
        ui.separator()
        with ui.row(align_items="start"):
            stats_widget(state.current_player.unwrap())
            related_widget(state.similar_players.unwrap())

    ui.run()

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
    with ui.card():
        ui.label("PLAYER STATS")
        ui.label(f"Goals: {player.goals}")
        ui.label(f"Assists: {player.assists}")
        ui.label(f"Sofascore Rating: {player.rating}")

def related_widget(similar_players: list[PlayerData]):
    with ui.card():
        ui.label("SIMILAR PLAYERS")
        
        for player in similar_players[:3]:
            ui.label(player.name)
