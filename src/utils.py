from pathlib import Path


def get_player_image(player_id: int) -> Path:
    return Path(f"data/images/{player_id}.png")
