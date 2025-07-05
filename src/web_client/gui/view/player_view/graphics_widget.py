from nicegui import ui
from plotly import graph_objects as go
from nicegui.events import GenericEventArguments

from web_client.gui.controller.update import go_to_player_named
from web_client.gui.state.state import AppState
from web_client.gui.controller.networking import fetch_query


def graphics_widget(state: AppState):
    with ui.card().classes("full-width"):
        with ui.row(wrap=False).classes("full-width"):
            with ui.column():
                input_widget(state, "Filter", "graphic_filter")
                input_widget(state, "Y Axis", "graphic_column_a")
                input_widget(state, "X Axis", "graphic_column_b")
                ui.button("Update").on_click(plotly_graph.refresh)

            plotly_graph(state)
            
def input_widget(state: AppState, label: str, attribute: str) -> None:
	ui.input(label)\
	  .bind_value(state, attribute)\
	  .on("keydown.enter", plotly_graph.refresh())

@ui.refreshable
def plotly_graph(state: AppState) -> None:
	players = fetch_query(state.graphic_filter, state.graphic_column_a, state.graphic_column_b)\
		.alt(lambda x: print(x))\
		.value_or([])

	fig = go.Figure()

	for player in players:
		x, y = player.stats.values()
		fig.add_trace(go.Scatter(
			x=[x],
   			y=[y],
			showlegend=False,
			name=player.name,
      		mode="markers",
			marker=dict(
				size=15 if player.name == state.current_player.name else 8, # type: ignore
				color="red" if player.name == state.current_player.name else "blue" # type: ignore
			)
        ))

	plot = ui.plotly(fig).classes("w-full h-[600px]")
	plot.on('plotly_click', lambda x: go_to_player_named(state, get_name_from_event(x)))

@ui.refreshable
def get_name_from_event(event: GenericEventArguments) -> str:
	print(event.args["points"])
	return event.args["points"][0]["data"]["name"]
