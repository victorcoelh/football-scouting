import pandas as pd
import numpy as np
from numpy.linalg import norm


def most_similar_players(database: pd.DataFrame, player_id: int, criteria: list[str]) -> list[int]:
    player_data = database.iloc[player_id] # type: ignore
    player_data = player_data[criteria]
    
    other_players_by_similarity: list[tuple[int, float]] = []

    for other_id, other_data in database.iterrows():
        if other_id == player_id:
            continue
        
        similarity = cossine_similarity(player_data, other_data[criteria])
        other_players_by_similarity.append((other_id, similarity)) # type: ignore
        
    player_list = sorted(other_players_by_similarity, key=lambda x: x[1], reverse=True)
    return list(map(lambda x: x[0], player_list))

def cossine_similarity(player: pd.Series, other: pd.Series) -> float:
    a = player.to_numpy()
    b = other.to_numpy()

    return np.dot(a, b)/(norm(a)*norm(b))

def sort_by_column(dataset: pd.DataFrame, column_name: str) -> pd.DataFrame:
    return dataset.sort_values(column_name)

def filter_column(dataset: pd.DataFrame, column_name: str, value: str) -> pd.DataFrame:
    return dataset[dataset[column_name] == value]
