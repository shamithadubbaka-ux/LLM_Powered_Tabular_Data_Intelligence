import pandas as pd
import streamlit as st

from app.data_engine import (
    load_tabular_file,
    create_connection,
    execute_sql
)

from app.profiling import (
    build_profile
)

from app.quality import (
    run_quality_checks,
    calculate_quality_score
)

from app.sql_guard import (
    validate_read_only,
    apply_row_limit
)

from app.llm import (
    LLMService
)

from app.charting import (
    build_chart
)


st.set_page_config(
    page_title=
        "LLM-Powered Tabular Data Intelligence",

    page_icon="📊",

    layout="wide"
)


st.title(
    "📊 LLM-Powered Tabular Data Intelligence"
)

st.caption(
    "Natural language → safe SQL → "
    "deterministic analytics → explanation"
)


with st.sidebar:

    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ]
    )


if not uploaded:

    st.info(
        "Upload a dataset to begin."
    )

    st.markdown(
        """
### Example questions

- What is the total revenue?
- Which region generated the highest revenue?
- Show monthly revenue.
- What are the top 5 products by profit?
- Compare average sales by category.
"""
    )

    st.stop()


try:

    dataframe = load_tabular_file(
        uploaded.getvalue(),
        uploaded.name
    )

except Exception as exc:

    st.error(
        f"Could not load file: {exc}"
    )

    st.stop()


profile = build_profile(
    dataframe
)

quality = run_quality_checks(
    dataframe
)

quality_score = calculate_quality_score(
    quality,
    profile["rows"],
    profile["columns"]
)

connection = create_connection(
    dataframe
)


overview_tab, quality_tab, ask_tab, sql_tab = st.tabs(
    [
        "Overview",
        "Data Quality",
        "Ask Your Data",
        "SQL Console"
    ]
)


# ======================================
# OVERVIEW
# ======================================

with overview_tab:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        f"{profile['rows']:,}"
    )

    col2.metric(
        "Columns",
        f"{profile['columns']:,}"
    )

    col3.metric(
        "Duplicates",
        f"{profile['duplicate_rows']:,}"
    )

    col4.metric(
        "Quality",
        f"{quality_score}/100"
    )

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(
        dataframe.head(25),
        use_container_width=True
    )

    st.subheader(
        "Column Profile"
    )

    st.dataframe(
        pd.DataFrame(
            profile["columns_detail"]
        ),
        use_container_width=True
    )


# ======================================
# QUALITY
# ======================================

with quality_tab:

    st.metric(
        "Data Quality Score",
        f"{quality_score}/100"
    )

    st.subheader(
        "Missing Values"
    )

    st.dataframe(
        pd.DataFrame(
            quality["missing"]
        ),
        use_container_width=True
    )

    st.subheader(
        "Outliers"
    )

    st.dataframe(
        pd.DataFrame(
            quality["outliers"]
        ),
        use_container_width=True
    )

    st.write(
        "Constant columns:",
        quality["constant_columns"]
        or "None"
    )

    st.write(
        "High-cardinality columns:",
        quality["high_cardinality_columns"]
        or "None"
    )


# ======================================
# ASK
# ======================================

with ask_tab:

    question = st.text_input(
        "Ask a question about your dataset",
        placeholder=
            "Which region has the highest revenue?"
    )

    if (
        st.button(
            "Analyze",
            type="primary"
        )
        and question.strip()
    ):

        try:

            llm = LLMService()

            plan = llm.generate_plan(
                question,
                {
                    "table":
                        "uploaded_data",

                    "rows":
                        profile["rows"],

                    "columns":
                        profile["columns_detail"]
                }
            )

            generated_sql = plan.get(
                "sql",
                ""
            )

            valid, message = (
                validate_read_only(
                    generated_sql
                )
            )

            if not valid:

                st.error(
                    f"Generated SQL rejected: {message}"
                )

                st.code(
                    generated_sql,
                    language="sql"
                )

                st.stop()

            safe_sql = apply_row_limit(
                generated_sql
            )

            result = execute_sql(
                connection,
                safe_sql
            )

            st.subheader(
                "Result"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

            st.download_button(
                "Download Result as CSV",

                result.to_csv(
                    index=False
                ),

                "query_result.csv",

                "text/csv"
            )

            with st.expander(
                "Generated SQL"
            ):

                st.code(
                    safe_sql,
                    language="sql"
                )

                st.success(
                    "Read-only SQL validation passed."
                )

            figure = build_chart(
                result,
                plan.get("chart")
            )

            if figure:

                st.subheader(
                    "Visualization"
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True
                )

            st.subheader(
                "Analytical Explanation"
            )

            explanation = (
                llm.explain_result(
                    question,
                    safe_sql,
                    result
                    .head(50)
                    .to_dict(
                        orient="records"
                    ),
                    profile
                )
            )

            st.write(
                explanation
            )

        except Exception as exc:

            st.error(
                f"Analysis failed: {exc}"
            )


# ======================================
# SQL CONSOLE
# ======================================

with sql_tab:

    sql = st.text_area(
        "Read-only DuckDB SQL",

        value=(
            "SELECT * "
            "FROM uploaded_data "
            "LIMIT 20"
        ),

        height=180
    )

    if st.button(
        "Run SQL"
    ):

        valid, message = (
            validate_read_only(
                sql
            )
        )

        if not valid:

            st.error(
                message
            )

        else:

            try:

                result = execute_sql(
                    connection,
                    apply_row_limit(sql)
                )

                st.dataframe(
                    result,
                    use_container_width=True
                )

            except Exception as exc:

                st.error(
                    f"SQL execution failed: {exc}"
                )