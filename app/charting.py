import pandas as pd
import plotly.express as px


def build_chart(result, chart_spec):
    """
    Build a Plotly chart from an LLM-generated chart specification.

    Supported chart types:
    bar
    horizontal_bar
    line
    pie
    scatter
    grouped_bar
    stacked_bar
    area
    histogram
    box
    """

    if result is None or result.empty:
        return None

    if not chart_spec:
        return None

    if not isinstance(chart_spec, dict):
        return None

    chart_type = str(
        chart_spec.get("type", "")
    ).lower().strip()

    x_column = chart_spec.get("x")
    y_column = chart_spec.get("y")

    title = chart_spec.get(
        "title",
        "Data Visualization"
    )

    data = result.copy()

    # --------------------------------------------------
    # BAR CHART
    # --------------------------------------------------

    if chart_type == "bar":

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.bar(
            data,
            x=x_column,
            y=y_column,
            title=title
        )

    # --------------------------------------------------
    # HORIZONTAL BAR
    # --------------------------------------------------

    if chart_type in {
        "horizontal_bar",
        "horizontal bar"
    }:

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.bar(
            data,
            x=y_column,
            y=x_column,
            orientation="h",
            title=title
        )

    # --------------------------------------------------
    # LINE CHART
    # --------------------------------------------------

    if chart_type == "line":

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.line(
            data,
            x=x_column,
            y=y_column,
            markers=True,
            title=title
        )

    # --------------------------------------------------
    # PIE CHART
    # --------------------------------------------------

    if chart_type == "pie":

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.pie(
            data,
            names=x_column,
            values=y_column,
            title=title
        )

    # --------------------------------------------------
    # SCATTER PLOT
    # --------------------------------------------------

    if chart_type == "scatter":

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.scatter(
            data,
            x=x_column,
            y=y_column,
            title=title
        )

    # --------------------------------------------------
    # GROUPED BAR
    # --------------------------------------------------

    if chart_type in {
        "grouped_bar",
        "grouped bar"
    }:

        if x_column not in data.columns:
            return None

        # Multiple Y columns
        y_columns = chart_spec.get("y_columns")

        if y_columns:

            valid_columns = [
                column
                for column in y_columns
                if column in data.columns
            ]

            if len(valid_columns) < 2:
                return None

            melted = data.melt(
                id_vars=[x_column],
                value_vars=valid_columns,
                var_name="Metric",
                value_name="Value"
            )

            return px.bar(
                melted,
                x=x_column,
                y="Value",
                color="Metric",
                barmode="group",
                title=title
            )

        # Single Y column with a grouping column
        group_column = chart_spec.get("group")

        if (
            group_column
            and group_column in data.columns
            and y_column
            and y_column in data.columns
        ):

            return px.bar(
                data,
                x=x_column,
                y=y_column,
                color=group_column,
                barmode="group",
                title=title
            )

        return None

    # --------------------------------------------------
    # STACKED BAR
    # --------------------------------------------------

    if chart_type in {
        "stacked_bar",
        "stacked bar"
    }:

        if x_column not in data.columns:
            return None

        y_columns = chart_spec.get("y_columns")

        if not y_columns:
            return None

        valid_columns = [
            column
            for column in y_columns
            if column in data.columns
        ]

        if len(valid_columns) < 2:
            return None

        melted = data.melt(
            id_vars=[x_column],
            value_vars=valid_columns,
            var_name="Metric",
            value_name="Value"
        )

        return px.bar(
            melted,
            x=x_column,
            y="Value",
            color="Metric",
            barmode="stack",
            title=title
        )

    # --------------------------------------------------
    # AREA CHART
    # --------------------------------------------------

    if chart_type == "area":

        if not x_column or not y_column:
            return None

        if x_column not in data.columns:
            return None

        if y_column not in data.columns:
            return None

        return px.area(
            data,
            x=x_column,
            y=y_column,
            title=title
        )

    # --------------------------------------------------
    # HISTOGRAM
    # --------------------------------------------------

    if chart_type == "histogram":

        column = chart_spec.get(
            "column",
            x_column
        )

        if not column:
            return None

        if column not in data.columns:
            return None

        return px.histogram(
            data,
            x=column,
            title=title
        )

    # --------------------------------------------------
    # BOX PLOT
    # --------------------------------------------------

    if chart_type in {
        "box",
        "box_plot",
        "box plot"
    }:

        if not y_column:
            y_column = x_column

        if not y_column:
            return None

        if y_column not in data.columns:
            return None

        return px.box(
            data,
            y=y_column,
            title=title
        )

    # --------------------------------------------------
    # UNKNOWN CHART
    # --------------------------------------------------

    return None