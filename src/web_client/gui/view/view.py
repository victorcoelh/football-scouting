from nicegui import ui

from web_client.gui.state.state import AppState
from web_client.gui.view.dashboard.dashboard import dashboard
from web_client.gui.view.player_view.player_view import player_screen
from web_client.gui.view.side_panel import create_sidebar


def view(state: AppState) -> None:
    ui.dark_mode(True)
    ui.add_head_html("<style>body {background-color: #131722; }</style>")
    create_sidebar("Victor", "v.coelhods@gmail.com")
    main_window(state)

    state.subscribe(main_window.refresh, "current_player")

@ui.refreshable
def main_window(state: AppState) -> None:
    match state.current_player:
        case None:
            dashboard(state)
        case _:
            player_screen(state)
