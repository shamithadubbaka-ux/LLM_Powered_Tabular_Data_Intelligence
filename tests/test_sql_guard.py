from app.sql_guard import validate_read_only


def test_select_is_allowed():

    valid, _ = validate_read_only(
        "SELECT * FROM uploaded_data"
    )

    assert valid


def test_with_is_allowed():

    valid, _ = validate_read_only(
        """
        WITH data AS (
            SELECT 1 AS value
        )
        SELECT * FROM data
        """
    )

    assert valid


def test_drop_is_blocked():

    valid, _ = validate_read_only(
        "DROP TABLE uploaded_data"
    )

    assert not valid


def test_insert_is_blocked():

    valid, _ = validate_read_only(
        "INSERT INTO uploaded_data VALUES (1)"
    )

    assert not valid


def test_multiple_statements_are_blocked():

    valid, _ = validate_read_only(
        "SELECT 1; SELECT 2"
    )

    assert not valid