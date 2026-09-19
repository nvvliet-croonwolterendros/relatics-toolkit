import pandas as pd
from pandas.testing import assert_frame_equal

from relatics_toolkit.processing.validator import normalize_tables


def test_normalize_tables_skips_missing_tables():
    """Return no output for schema tables not present in the input."""
    schema = {
        "table_one": {
            "column_one": {"normalize": True},
        }
    }

    result = normalize_tables({}, schema)

    assert result == {}


def test_normalize_tables_drops_empty_rows():
    """Drop rows where all column values are missing."""
    schema = {
        "table_one": {
            "column_one": {"normalize": False},
        }
    }

    tables = {"table_one": pd.DataFrame({"column_one": ["value", None]})}

    expected = pd.DataFrame({"column_one": ["value"]}).reset_index(drop=True)

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_normalize_value():
    """Normalizes values only for columns configured with normalize=True."""
    schema = {
        "table_one": {
            "column_one": {"normalize": True},
            "column_two": {},
            "column_three": {"normalize": False},
        }
    }

    tables = {
        "table_one": pd.DataFrame(
            {
                "column_one": ["Value One"],
                "column_two": ["Value Two"],
                "column_three": ["Value Three"],
            }
        )
    }

    expected = pd.DataFrame(
        {
            "column_one": ["value_one"],
            "column_two": ["Value Two"],
            "column_three": ["Value Three"],
        }
    )

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_missing_column():
    """Adds missing schema columns and initializes them with None."""
    schema = {"table_one": {"column_one": {"normalize": True}, "column_two": {}}}

    tables = {"table_one": pd.DataFrame({"column_one": ["Value One"]})}

    expected = pd.DataFrame({"column_one": ["value_one"], "column_two": [None]})

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_missing_column_no_rows():
    """Adds missing schema columns to an empty table without creating rows."""
    schema = {
        "table_one": {
            "column_one": {"normalize": True},
        }
    }

    tables = {"table_one": pd.DataFrame()}

    expected = pd.DataFrame(columns=["column_one"])

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_drop_all_null_rows():
    """Removes rows that contain only missing values after normalization."""
    schema = {
        "table_one": {
            "column_one": {"normalize": True},
        }
    }

    tables = {"table_one": pd.DataFrame({"column_one": [None]})}

    expected = pd.DataFrame(columns=["column_one"])

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)
