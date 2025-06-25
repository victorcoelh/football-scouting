from nicegui import ui
from plotly import graph_objects as go

from web_client.gui.state.state import AppState
from web_client.gui.controller.networking import fetch_query


def graphics_widget(state: AppState):
    with ui.card():
        with ui.row():
            with ui.column():
                ui.input("filter")\
                  .bind_value(state, "graphic_filter")\
                  .on("keydown.enter", )

                ui.input("column_a")\
                  .bind_value(state, "graphic_column_a")

                ui.input("column_b")\
                  .bind_value(state, "graphic_column_b")
                  
            plotly_graph(state)
            state.subscribe(plotly_graph.refresh, "graphic_filter")
            state.subscribe(plotly_graph.refresh, "graphic_column_a")
            state.subscribe(plotly_graph.refresh, "graphic_column_b")

@ui.refreshable
def plotly_graph(state: AppState):
    data = fetch_query(state.graphic_filter, state.graphic_column_a, state.graphic_column_b)
    
    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
    ui.plotly(fig)


if __name__ in {"__main__", "__mp_main__"}:
    state = AppState()
    
    ui.dark_mode(True)
    graphics_widget(state)
    ui.run()
