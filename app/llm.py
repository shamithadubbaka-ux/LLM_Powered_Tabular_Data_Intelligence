import json
import os
import re

from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

        self.client = None

        if self.api_key:
            try:
                from groq import Groq

                self.client = Groq(
                    api_key=self.api_key
                )
            except ImportError:
                self.client = None

    # ==========================================================
    # GENERATE SQL + CHART PLAN
    # ==========================================================

    def generate_plan(self, question, schema):

        if not self.client:
            raise RuntimeError(
                "Groq is not configured. "
                "Add GROQ_API_KEY to your .env file."
            )

        columns = schema.get("columns", [])

        prompt = f"""
You are an expert data analyst and DuckDB SQL developer.

Your task is to convert ONE natural-language question
into ONE correct DuckDB SQL query and an appropriate
visualization specification.

==================================================
TABLE
==================================================

uploaded_data

==================================================
SCHEMA
==================================================

{json.dumps(columns, indent=2, default=str)}

==================================================
USER QUESTION
==================================================

{question}

==================================================
SQL RULES
==================================================

1. Generate exactly ONE SQL query.

2. The query must begin with SELECT or WITH.

3. The query must be valid DuckDB SQL.

4. Only read data.

5. Only use this table:

uploaded_data

6. Only use columns that exist in the provided schema.

7. Never modify the data.

8. NEVER use:

INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
COPY
INSTALL
LOAD
ATTACH
DETACH
GRANT
REVOKE
MERGE
REPLACE

9. Do not generate multiple SQL statements.

10. Do not generate unnecessary UNION or UNION ALL.

11. Never put LIMIT before UNION or UNION ALL.

12. For highest/top questions use:

ORDER BY ... DESC
LIMIT ...

13. For lowest/bottom questions use:

ORDER BY ... ASC
LIMIT ...

14. For total questions use SUM().

15. For average questions use AVG().

16. For counting questions use COUNT().

17. For distinct counting use COUNT(DISTINCT column).

18. For category comparisons use GROUP BY.

19. For ranking questions use ORDER BY and LIMIT.

20. Use clear aliases for calculated columns.

==================================================
DUCKDB DATE RULES
==================================================

This is DuckDB SQL.

DO NOT use:

to_date()
to_datetime()
STR_TO_DATE()
DATE_FORMAT()

For date strings use:

CAST(column AS DATE)

If invalid dates may exist use:

TRY_CAST(column AS DATE)

For monthly aggregation use:

date_trunc('month', CAST(column AS DATE))

For yearly aggregation use:

date_trunc('year', CAST(column AS DATE))

For quarterly aggregation use:

date_trunc('quarter', CAST(column AS DATE))

Example:

SELECT
    date_trunc(
        'month',
        CAST(Date AS DATE)
    ) AS month,
    SUM(Revenue) AS total_revenue
FROM uploaded_data
GROUP BY month
ORDER BY month

==================================================
CHART SELECTION
==================================================

Choose the visualization based on the user's question.

The chart specification MUST reference columns
that actually exist in the SQL result.

--------------------------------------------------
1. BAR CHART
--------------------------------------------------

Use:

"type": "bar"

for categorical comparisons.

Example question:

Compare revenue by region.

Expected chart:

{{
    "type": "bar",
    "x": "Region",
    "y": "TotalRevenue",
    "title": "Revenue by Region"
}}

--------------------------------------------------
2. HORIZONTAL BAR
--------------------------------------------------

Use:

"type": "horizontal_bar"

for rankings and Top-N questions.

Example:

Top 10 products by revenue.

Expected:

{{
    "type": "horizontal_bar",
    "x": "Product",
    "y": "TotalRevenue",
    "title": "Top 10 Products by Revenue"
}}

The SQL should return Product and TotalRevenue.

--------------------------------------------------
3. LINE CHART
--------------------------------------------------

Use:

"type": "line"

for trends over time.

Examples:

Show monthly revenue.

Show yearly sales.

Show revenue trend by month.

Expected:

{{
    "type": "line",
    "x": "month",
    "y": "total_revenue",
    "title": "Monthly Revenue"
}}

--------------------------------------------------
4. PIE CHART
--------------------------------------------------

Use:

"type": "pie"

for percentage, share, contribution,
or part-of-whole questions.

Example:

What percentage of sales comes from each category?

Expected:

{{
    "type": "pie",
    "x": "Category",
    "y": "TotalSales",
    "title": "Sales by Category"
}}

Use pie charts only when there are a reasonable
number of categories.

--------------------------------------------------
5. SCATTER PLOT
--------------------------------------------------

Use:

"type": "scatter"

when comparing the relationship between
two numeric variables.

Example:

Show revenue vs profit.

Expected:

{{
    "type": "scatter",
    "x": "Revenue",
    "y": "Profit",
    "title": "Revenue vs Profit"
}}

--------------------------------------------------
6. GROUPED BAR
--------------------------------------------------

Use:

"type": "grouped_bar"

when comparing multiple metrics across
categories.

Example:

Compare sales and profit by region.

The SQL should return:

Region
Sales
Profit

Expected:

{{
    "type": "grouped_bar",
    "x": "Region",
    "y_columns": [
        "Sales",
        "Profit"
    ],
    "title": "Sales vs Profit by Region"
}}

--------------------------------------------------
7. STACKED BAR
--------------------------------------------------

Use:

"type": "stacked_bar"

when multiple measures or categories
represent components of a combined total.

Example:

Show sales composition by region.

Use:

{{
    "type": "stacked_bar",
    "x": "Region",
    "y_columns": [
        "OnlineSales",
        "StoreSales"
    ],
    "title": "Sales Composition by Region"
}}

--------------------------------------------------
8. AREA CHART
--------------------------------------------------

Use:

"type": "area"

for cumulative or volume-style trends,
especially over time.

Example:

Show cumulative revenue over time.

Expected:

{{
    "type": "area",
    "x": "month",
    "y": "cumulative_revenue",
    "title": "Cumulative Revenue"
}}

--------------------------------------------------
9. HISTOGRAM
--------------------------------------------------

Use:

"type": "histogram"

when the user asks about the distribution
of a numeric variable.

Example:

Show the distribution of revenue.

Expected:

{{
    "type": "histogram",
    "column": "Revenue",
    "title": "Revenue Distribution"
}}

--------------------------------------------------
10. BOX PLOT
--------------------------------------------------

Use:

"type": "box"

when the user asks about:

- distribution
- spread
- median
- outliers
- variability

Example:

Show the distribution and outliers of profit.

Expected:

{{
    "type": "box",
    "x": "Region",
    "y": "Profit",
    "title": "Profit Distribution"
}}

==================================================
CHART RULES
==================================================

1. Always return a chart specification when
visualization is useful.

2. Return:

"chart": null

only when visualization is genuinely not useful.

3. Never invent chart column names.

4. Every chart column must exist in the SQL result.

5. For grouped_bar use:

y_columns

6. For stacked_bar use:

y_columns

7. For horizontal_bar use:

x = category
y = numeric measure

8. For pie use:

x = category
y = numeric value

9. For scatter use:

x = numeric column
y = numeric column

10. For line charts use a time/date column
when the question concerns time.

==================================================
IMPORTANT SQL + CHART CONSISTENCY
==================================================

The chart specification must match the SQL output.

For example, if the chart says:

"x": "Region"
"y": "TotalRevenue"

then the SQL MUST return:

Region
TotalRevenue

Do not return:

Revenue

if the chart expects:

TotalRevenue

==================================================
EXAMPLES
==================================================

QUESTION:

Which region generated the highest revenue?

SQL:

SELECT
    Region,
    SUM(Revenue) AS TotalRevenue
FROM uploaded_data
GROUP BY Region
ORDER BY TotalRevenue DESC
LIMIT 1

CHART:

{{
    "type": "bar",
    "x": "Region",
    "y": "TotalRevenue",
    "title": "Highest Revenue by Region"
}}

--------------------------------------------------

QUESTION:

Show monthly revenue.

SQL:

SELECT
    date_trunc(
        'month',
        CAST(Date AS DATE)
    ) AS month,
    SUM(Revenue) AS total_revenue
FROM uploaded_data
GROUP BY month
ORDER BY month

CHART:

{{
    "type": "line",
    "x": "month",
    "y": "total_revenue",
    "title": "Monthly Revenue"
}}

--------------------------------------------------

QUESTION:

Top 10 products by revenue.

SQL:

SELECT
    Product,
    SUM(Revenue) AS TotalRevenue
FROM uploaded_data
GROUP BY Product
ORDER BY TotalRevenue DESC
LIMIT 10

CHART:

{{
    "type": "horizontal_bar",
    "x": "Product",
    "y": "TotalRevenue",
    "title": "Top 10 Products by Revenue"
}}

--------------------------------------------------

QUESTION:

Compare sales and profit by region.

SQL:

SELECT
    Region,
    SUM(Sales) AS Sales,
    SUM(Profit) AS Profit
FROM uploaded_data
GROUP BY Region
ORDER BY Region

CHART:

{{
    "type": "grouped_bar",
    "x": "Region",
    "y_columns": [
        "Sales",
        "Profit"
    ],
    "title": "Sales vs Profit by Region"
}}

--------------------------------------------------

QUESTION:

Show revenue vs profit.

SQL:

SELECT
    Revenue,
    Profit
FROM uploaded_data

CHART:

{{
    "type": "scatter",
    "x": "Revenue",
    "y": "Profit",
    "title": "Revenue vs Profit"
}}

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do NOT return:

- Markdown
- code fences
- explanations
- comments
- "Here is the JSON"
- additional text

Return exactly:

{{
    "sql": "SELECT ...",
    "chart": {{
        "type": "bar",
        "x": "column_name",
        "y": "column_name",
        "title": "Chart title"
    }}
}}

OR:

{{
    "sql": "SELECT ...",
    "chart": null
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise DuckDB SQL generator "
                        "and tabular analytics planner. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={
                "type": "json_object"
            }
        )

        content = response.choices[0].message.content

        return self._parse_json(content)

    # ==========================================================
    # EXPLAIN RESULT
    # ==========================================================

    def explain_result(
        self,
        question,
        sql,
        result,
        profile
    ):

        if not self.client:
            return (
                "The query was executed successfully. "
                "Add GROQ_API_KEY to enable "
                "AI-generated explanations."
            )

        prompt = f"""
You are a professional data analyst.

Explain the result of a database query.

USER QUESTION:
{question}

SQL:
{sql}

QUERY RESULT:
{json.dumps(result, indent=2, default=str)}

DATASET PROFILE:
{json.dumps(profile, indent=2, default=str)}

Rules:

1. Use only information present in the query result.

2. Do not invent values.

3. Do not make unsupported assumptions.

4. Mention important numbers when useful.

5. Keep the explanation concise.

6. Clearly describe what the result means.

7. If the result contains rankings, mention the
relevant ranking.

8. If the result shows a trend, describe the trend
using only the available values.

9. Do not provide unrelated advice.

Return normal plain text.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You explain tabular analytics results "
                        "accurately and concisely."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    # ==========================================================
    # ROBUST JSON PARSER
    # ==========================================================

    @staticmethod
    def _parse_json(content):

        if not content:
            raise ValueError(
                "LLM returned an empty response."
            )

        content = content.strip()

        # Remove Markdown code fences
        content = re.sub(
            r"^```(?:json)?\s*",
            "",
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r"\s*```$",
            "",
            content
        )

        content = content.strip()

        # ----------------------------------------------
        # Attempt 1: entire response is JSON
        # ----------------------------------------------

        try:
            parsed = json.loads(content)

            if not isinstance(parsed, dict):
                raise ValueError(
                    "LLM JSON response is not an object."
                )

            return parsed

        except json.JSONDecodeError:
            pass

        # ----------------------------------------------
        # Attempt 2: extract JSON object
        # ----------------------------------------------

        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1 and end > start:

            json_text = content[
                start:end + 1
            ]

            try:

                parsed = json.loads(json_text)

                if not isinstance(parsed, dict):
                    raise ValueError(
                        "LLM JSON response is not an object."
                    )

                return parsed

            except json.JSONDecodeError:
                pass

        # ----------------------------------------------
        # Helpful error
        # ----------------------------------------------

        preview = content[:500]

        preview = preview.replace(
            "\n",
            " "
        )

        raise ValueError(
            "LLM returned invalid JSON. "
            f"Response started with: {preview}"
        )