import pandas as pd
from db import engine

def load_transactions():

    query = """
    SELECT TOP 5000 *
    FROM transactions
    ORDER BY transaction_date DESC
    """

    df = pd.read_sql(query, engine)

    return df