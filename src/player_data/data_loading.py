import pandas as pd
from numpy.linalg import norm


def load_data() -> pd.DataFrame:
    database = pd.read_csv("data/mock_data.csv", index_col=0)        
    return database

def normalize_data(database: pd.DataFrame) -> pd.DataFrame:
    normalized_data = pd.DataFrame()

    for column in database.columns:
        if database[column].dtype == "object":
            normalized_data[column] = database[column]
        else:
            normalized_data[column] = database[column].map(lambda x: x / norm(database[column]))
    return normalized_data
