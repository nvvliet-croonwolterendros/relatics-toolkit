import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from relatics_toolkit.processing.validator import normalize_tables, validate_schema


def test_normalize_tables_skips_missing_tables():
    """Return no output for schema tables not present in the input."""
    schema = {
        "table_one": {
            "columns": {
                "column_one": {"normalize": True},
            }
        }
    }

    result = normalize_tables({}, schema)

    assert result == {}


def test_normalize_tables_drops_empty_rows():
    """Drop rows where all column values are missing."""
    schema = {
        "table_one": {
            "columns": {
                "column_one": {"normalize": False},
            }
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
            "columns": {
                "column_one": {"normalize": True},
                "column_two": {},
                "column_three": {"normalize": False},
            }
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
    schema = {
        "table_one": {"columns": {"column_one": {"normalize": True}, "column_two": {}}}
    }

    tables = {"table_one": pd.DataFrame({"column_one": ["Value One"]})}

    expected = pd.DataFrame({"column_one": ["value_one"], "column_two": [None]})

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_missing_column_no_rows():
    """Adds missing schema columns to an empty table without creating rows."""
    schema = {
        "table_one": {
            "columns": {
                "column_one": {"normalize": True},
            }
        }
    }

    tables = {"table_one": pd.DataFrame()}

    expected = pd.DataFrame(columns=["column_one"])

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_normalize_tables_drop_all_null_rows():
    """Removes rows that contain only missing values."""
    schema = {
        "table_one": {
            "columns": {
                "column_one": {"normalize": True},
            }
        }
    }

    tables = {"table_one": pd.DataFrame({"column_one": [None]})}

    expected = pd.DataFrame(columns=["column_one"])

    result = normalize_tables(tables, schema)

    assert_frame_equal(result["table_one"], expected)


def test_validate_schema_raises_on_missing_table():
    """Raise an error when a required table is missing."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
            },
        }
    }

    tables = {}

    expected_errors = {
        "missing_tables": [
            {
                "table": "Person",
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_raises_on_missing_columns():
    """Raise an error when a required column is missing."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["Tim", "John", "John"],
            }
        )
    }

    expected_errors = {"missing_columns": [{"table": "Person", "columns": ["city"]}]}

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_raises_on_null_columns():
    """Raise an error when a not-null column contains null values."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["Tim", "John", None],
                "city": ["NL", "UK", "DE"],
            }
        )
    }

    expected_errors = {"null_values": [{"table": "Person", "columns": ["name"]}]}

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_accepts_unique_composite():
    """Accept rows with unique composite key values."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["Tim", "John", "John"],
                "city": ["NL", "UK", "DE"],
            }
        )
    }

    validate_schema(tables, schema)


def test_validate_schema_raises_on_duplicate_nulls():
    """Allow duplicate null values in a unique column."""
    schema = {
        "Person": {
            "columns": {
                "id": {"not_null": True},
                "name": {"not_null": False},
                "city": {"not_null": False},
            },
            "unique": [
                ["name"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "id": [1, 2, 3],
                "name": ["Tim", None, None],
                "city": ["NL", "UK", "DE"],
            }
        )
    }

    expected_errors = {
        "duplicate_values": [
            {
                "table": "Person",
                "columns": ["name"],
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_raises_on_duplicate_composite_nulls():
    """Allow duplicate composite keys when all key values are null."""
    schema = {
        "Person": {
            "columns": {
                "id": {"not_null": True},
                "name": {"not_null": False},
                "city": {"not_null": False},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "id": [1, 2, 3],
                "name": ["Tim", None, None],
                "city": ["NL", None, None],
            }
        )
    }

    expected_errors = {
        "duplicate_values": [
            {
                "table": "Person",
                "columns": ["name", "city"],
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_raises_on_duplicate_composite():
    """Raise an error when a composite unique constraint is violated."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["Tim", "John", "John"],
                "city": ["NL", "UK", "UK"],
            }
        )
    }

    expected_errors = {
        "duplicate_values": [
            {
                "table": "Person",
                "columns": ["name", "city"],
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_raises_on_duplicate_single_column():
    """Raise an error when a unique column contains duplicate values."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
            },
            "unique": [
                ["name"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["Tim", "John", "John"],
            }
        )
    }

    expected_errors = {
        "duplicate_values": [
            {
                "table": "Person",
                "columns": ["name"],
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_collects_multiple_errors():
    """Collect all validation errors before raising."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": ["John", "John", None],
                "city": ["UK", "UK", "DE"],
            }
        )
    }

    expected_errors = {
        "null_values": [
            {
                "table": "Person",
                "columns": ["name"],
            }
        ],
        "duplicate_values": [
            {
                "table": "Person",
                "columns": ["name", "city"],
            }
        ],
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors


def test_validate_schema_stops_table_validation_after_missing_columns():
    """Skip further validation when required columns are missing."""
    schema = {
        "Person": {
            "columns": {
                "name": {"not_null": True},
                "city": {"not_null": True},
            },
            "unique": [
                ["name", "city"],
            ],
        }
    }

    tables = {
        "Person": pd.DataFrame(
            {
                "name": [None, None],
            }
        )
    }

    expected_errors = {
        "missing_columns": [
            {
                "table": "Person",
                "columns": ["city"],
            }
        ]
    }

    with pytest.raises(RuntimeError) as exc_info:
        validate_schema(tables, schema)

    assert exc_info.value.args[0] == expected_errors
