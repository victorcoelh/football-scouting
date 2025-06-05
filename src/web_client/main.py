from returns.maybe import Nothing
from nicegui import ui

from web_client.gui.state import AppState
from web_client.gui.view import main_window
from web_client.gui.update import fetch_similar_players


def main() -> None:
    state = AppState(Nothing, Nothing)
    main_window(state)
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    print(fetch_similar_players(0))
