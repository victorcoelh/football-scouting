import pandas as pd
from numpy.linalg import norm


def load_data(csv_path: str) -> pd.DataFrame:
    database = pd.read_csv(csv_path)
    return database

def normalize_data(database: pd.DataFrame) -> pd.DataFrame:
    normalized_data = pd.DataFrame()

    for column in database.columns:
        if database[column].dtype == "object":
            normalized_data[column] = database[column]
        else:
            normalized_data[column] = database[column].map(lambda x: x / norm(database[column]))
    return normalized_data
