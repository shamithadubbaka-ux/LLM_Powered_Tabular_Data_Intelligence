import pandas as pd


def run_quality_checks(dataframe):
    """
    Run basic data-quality checks on the uploaded dataset.
    """

    # Missing values
    missing = []

    for column in dataframe.columns:
        missing_count = int(dataframe[column].isna().sum())

        missing.append(
            {
                "column": column,
                "missing_count": missing_count,
                "missing_percent": round(
                    float(
                        dataframe[column].isna().mean() * 100
                    ),
                    2
                )
            }
        )

    # Outliers using the IQR method
    outliers = []

    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        series = dataframe[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        count = int(
            (
                (series < lower_bound)
                | (series > upper_bound)
            ).sum()
        )

        outliers.append(
            {
                "column": column,
                "outlier_count": count,
                "lower_bound": round(
                    float(lower_bound),
                    2
                ),
                "upper_bound": round(
                    float(upper_bound),
                    2
                )
            }
        )

    # Constant columns
    constant_columns = [
        column
        for column in dataframe.columns
        if dataframe[column].nunique(dropna=False) <= 1
    ]

    # High-cardinality columns
    high_cardinality_columns = []

    row_count = len(dataframe)

    if row_count > 0:

        for column in dataframe.columns:

            unique_count = dataframe[column].nunique(
                dropna=True
            )

            if unique_count / row_count >= 0.9:
                high_cardinality_columns.append(
                    column
                )

    return {
        "missing": missing,
        "outliers": outliers,
        "constant_columns": constant_columns,
        "high_cardinality_columns": high_cardinality_columns
    }


def calculate_quality_score(
    quality,
    rows,
    columns
):
    """
    Calculate a simple 0-100 data-quality score.
    """

    if rows == 0 or columns == 0:
        return 0

    score = 100.0

    # Missing-value penalty
    total_missing = sum(
        item["missing_count"]
        for item in quality["missing"]
    )

    total_cells = rows * columns

    missing_ratio = (
        total_missing / total_cells
        if total_cells > 0
        else 0
    )

    score -= min(
        missing_ratio * 50,
        30
    )

    # Duplicate penalty
    duplicate_count = quality.get(
        "duplicate_rows",
        0
    )

    if duplicate_count:
        score -= min(
            duplicate_count / rows * 20,
            20
        )

    # Constant-column penalty
    score -= min(
        len(quality["constant_columns"]) * 5,
        15
    )

    # Outlier penalty
    total_outliers = sum(
        item["outlier_count"]
        for item in quality["outliers"]
    )

    if rows > 0:
        outlier_ratio = (
            total_outliers / rows
        )

        score -= min(
            outlier_ratio * 20,
            15
        )

    return round(
        max(0, min(100, score)),
        2
    )