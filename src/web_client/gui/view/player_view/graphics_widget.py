from nicegui import ui
from plotly import graph_objects as go
from nicegui.events import GenericEventArguments

from web_client.gui.controller.update import go_to_player_named
from web_client.gui.state.state import AppState
from web_client.gui.controller.networking import fetch_query


def graphics_widget(state: AppState):
    with ui.card().classes("full-width"):
        with ui.row():
            with ui.column():
                input_widget(state, "Filter", "graphic_filter")
                input_widget(state, "Column A", "graphic_column_a")
                input_widget(state, "Column B", "graphic_column_b")
                ui.button("Update").on_click(plotly_graph.refresh)

            plotly_graph(state)
            
def input_widget(state: AppState, label: str, attribute: str) -> None:
	ui.input(label)\
	  .bind_value(state, attribute)\
	  .on("keydown.enter", plotly_graph.refresh())

@ui.refreshable
def plotly_graph(state: AppState) -> None:
    _, names, x, y = fetch_query(state.graphic_filter, state.graphic_column_a, state.graphic_column_b)\
      .alt(lambda x: print(x))\
      .value_or((None, "ass", None, None))

    colors = ["red" if name == state.current_player.name else "blue" for name in names] # type: ignore
    sizes = [15 if name == state.current_player.name else 8 for name in names] # type: ignore
    
    fig = go.Figure(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        text=names,
        marker=dict(
          size=12,
          color=colors
        )
    ))

    plot = ui.plotly(fig)
    plot.on('plotly_click', lambda x: go_to_player_named(state, get_name_from_event(x)))

def get_name_from_event(event: GenericEventArguments) -> str:
  return event.args["points"][0]["text"]
