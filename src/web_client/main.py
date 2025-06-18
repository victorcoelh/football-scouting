from nicegui import ui

from web_client.gui.state.state import AppState
from web_client.gui.view.view import view


def main() -> None:
    state = AppState()
    view(state)
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
