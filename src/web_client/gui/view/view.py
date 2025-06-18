from nicegui import ui

from web_client.gui.state.state import AppState
from web_client.gui.view.dashboard import dashboard
from web_client.gui.view.player_view import player_screen


def view(state: AppState) -> None:
    main_window(state)
    state.subscribe(main_window.refresh, "current_player")

@ui.refreshable
def main_window(state: AppState) -> None:
    match state.current_player:
        case None:
            dashboard(state)
        case _:
            player_screen(state)
