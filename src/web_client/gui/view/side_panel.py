from nicegui import ui

from web_client.gui.controller.update import go_to_dashboard, go_to_player_named
from web_client.gui.state.state import AppState


def create_sidebar(state: AppState, user_name: str, user_email: str):
    with ui.left_drawer().style("background-color: #1B2130")\
           .classes("w-[1200px] p-0"):

        with ui.column().classes("w-full p-5 pb-0"):
            ui.image("./assets/transfermatch_logo.png").classes('w-218')
            search_bar(state)
            nav_bar(state)

        user_widget(user_name, user_email)

def search_bar(state: AppState):
    textbox = ui.input(placeholder="Search") \
        .props('dense borderless input-style="color: #676D7C;"') \
        .classes("w-full") \
        .style("border-radius: 8px; background-color: #131722") \
        .on("keydown.enter", lambda event: go_to_player_named(state, event.sender.value))  # type: ignore
        
    with textbox.add_slot("prepend"):
        ui.icon("search", size="md")\
          .classes("ml-2")\
          .style("color: #676D7C")

def nav_bar(state: AppState):
    with ui.column().classes("w-full justify-center mt-20"):
        with ui.row().classes("w-full items-center hover:bg-slate-700 p-2 rounded-md")\
          .on("click", lambda: go_to_dashboard(state)):
            ui.icon("table_view", size="md").classes("text-white")
            ui.label("Player Database").classes("text-white text-lg")

        with ui.row().classes("w-full items-center hover:bg-slate-700 p-2 rounded-md")\
          .on('click', lambda: go_to_player_named(state, "Rodrigo Garro")):
            ui.icon("person", size="md").classes("text-white")
            ui.label("Player").classes("text-white text-lg")

        with ui.row().classes("w-full items-center hover:bg-slate-700 p-2 rounded-md"):
            ui.icon("assessment", size="md").classes("text-white")
            ui.label("Squad").classes("text-white text-lg")

        ui.separator().classes("my-4").style("color: white; size: 5px")

        with ui.row().classes("w-full items-center hover:bg-slate-700 p-2 rounded-md"):
            ui.icon("settings", size="md").classes("text-white")
            ui.label("Settings").classes("text-white text-lg")

def user_widget(user_name: str, user_email: str):
    with ui.card().classes("w-full h-[100px]").style("background-color: #2C3545; margin-top: auto"):
        with ui.row(wrap=False).classes("items-center h-full"):
            with ui.avatar():
                ui.image("./assets/placeholder_avatar.png").classes("w-16")

            with ui.column().style('gap: 0.05rem'):
                ui.label(user_name).classes("text-white text-lg font-bold my-0")
                ui.label(user_email).classes("text-gray-400 text-sm my-0")

            ui.space()
            ui.button(icon='logout', on_click=lambda: ui.notify('Logged off')) \
                .props('flat dense color=red') \
                .classes('ml-auto')
