import io

import duckdb
import pandas as pd


def load_tabular_file(file_bytes, filename):
    """
    Load a CSV or Excel file into a pandas DataFrame.
    """

    filename = filename.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(io.BytesIO(file_bytes))

    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(io.BytesIO(file_bytes))

    raise ValueError(
        "Unsupported file format. Please upload CSV or Excel."
    )


def create_connection(dataframe):
    """
    Create an in-memory DuckDB connection
    and register the uploaded DataFrame.
    """

    connection = duckdb.connect(database=":memory:")

    connection.register(
        "uploaded_data",
        dataframe
    )

    return connection


def execute_sql(connection, sql):
    """
    Execute read-only SQL and return the result as a DataFrame.
    """

    return connection.execute(sql).fetchdf()