import re


# SQL commands that are not allowed
BLOCKED_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "MERGE",
    "GRANT",
    "REVOKE",
    "ATTACH",
    "DETACH",
    "COPY",
    "INSTALL",
    "LOAD",
}


def validate_read_only(sql):
    """
    Validate that SQL contains only a single read-only query.

    Returns:
        (True, "OK") if the query is allowed.
        (False, reason) if the query is rejected.
    """

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    cleaned_sql = sql.strip()

    # Remove a trailing semicolon but reject multiple statements.
    cleaned_sql = cleaned_sql.rstrip(";").strip()

    if ";" in cleaned_sql:
        return (
            False,
            "Multiple SQL statements are not allowed."
        )

    # Remove SQL comments.
    no_comments = re.sub(
        r"--.*?$",
        "",
        cleaned_sql,
        flags=re.MULTILINE
    )

    no_comments = re.sub(
        r"/\*.*?\*/",
        "",
        no_comments,
        flags=re.DOTALL
    ).strip()

    if not no_comments:
        return False, "SQL query is empty."

    # The query must begin with SELECT or WITH.
    if not re.match(
        r"^(SELECT|WITH)\b",
        no_comments,
        flags=re.IGNORECASE
    ):
        return (
            False,
            "Only SELECT and WITH queries are allowed."
        )

    # Block dangerous SQL keywords.
    for keyword in BLOCKED_KEYWORDS:

        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(
            pattern,
            no_comments,
            flags=re.IGNORECASE
        ):
            return (
                False,
                f"Blocked SQL keyword: {keyword}"
            )

    return True, "OK"


def apply_row_limit(sql, limit=1000):
    """
    Add a maximum row limit to a SELECT query.

    If the query already contains LIMIT,
    it is left unchanged.
    """

    if not sql or not sql.strip():
        return sql

    cleaned_sql = sql.strip()

    if re.search(
        r"\bLIMIT\s+\d+\b",
        cleaned_sql,
        flags=re.IGNORECASE
    ):
        return cleaned_sql

    cleaned_sql = cleaned_sql.rstrip(";").strip()

    return (
        f"{cleaned_sql}\nLIMIT {limit}"
    )