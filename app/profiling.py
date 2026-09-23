import pandas as pd


def build_profile(dataframe):
    """
    Build a basic profile of the uploaded dataset.
    """

    rows = len(dataframe)
    columns = len(dataframe.columns)

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    columns_detail = []

    for column in dataframe.columns:

        series = dataframe[column]

        columns_detail.append(
            {
                "column": column,
                "data_type": str(series.dtype),
                "missing": int(series.isna().sum()),
                "missing_percent": round(
                    float(series.isna().mean() * 100),
                    2
                ),
                "unique_values": int(
                    series.nunique(dropna=True)
                )
            }
        )

    return {
        "rows": rows,
        "columns": columns,
        "duplicate_rows": duplicate_rows,
        "columns_detail": columns_detail
    }