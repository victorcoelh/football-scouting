# Football Scouting Platform

A web-based client and server for reading, analyzing and comparing different players across Brasileirão Série A and B.

### Installation

```
pip install uv
uv sync
uv pip install -e .
```

### Running

Starting the server:
```fastapi dev src/server/main.py```

Starting the web client:
```uv run src/web_client/main.py```
