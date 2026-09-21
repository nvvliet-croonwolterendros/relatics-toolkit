from collections import defaultdict

import pandas as pd

from relatics_toolkit.processing.schema import SCHEMA
from relatics_toolkit.utils.utils import normalize_value


def normalize_tables(
    tables: dict[str, pd.DataFrame],
    schema: dict[str, dict] = SCHEMA,
) -> dict[str, pd.DataFrame]:
    """
    Add columns to tables and normalize values according to the schema.

    Columns are added when missing and initialized with their default value
    if configured, else with None. Then values of columns are normalized if configured.
    """

    normalized_tables: dict[str, pd.DataFrame] = {}

    for table_name, table_rules in schema.items():
        table = tables.get(table_name)

        if table is not None:
            df = table.copy()

            df = df.dropna(how="all").reset_index(drop=True)

            for column_name, column_rules in table_rules.get("columns", {}).items():
                if column_name not in df.columns:
                    df[column_name] = column_rules.get("default", None)
                if column_rules.get("normalize"):
                    df[column_name] = df[column_name].apply(normalize_value)

            normalized_tables[table_name] = df

    return normalized_tables


def validate_schema(
    tables: dict[str, pd.DataFrame],
    schema: dict[str, dict],
) -> None:
    """
    Validate tables against the configured schema.

    Checks:
    - Required tables exist.
    - Required columns exist.
    - Columns marked 'not_null' contain no null values.
    - Columns/composites marked as unique contain no duplicates.
    """
    errors = defaultdict(list)

    for table_name, table_schema in schema.items():
        if table_name not in tables:
            errors["missing_tables"].append({"table": table_name})
            continue

        df = tables[table_name]

        column_schema = table_schema.get("columns", {})

        missing_columns = [
            column for column in column_schema if column not in df.columns
        ]

        if missing_columns:
            errors["missing_columns"].append(
                {
                    "table": table_name,
                    "columns": missing_columns,
                }
            )
            continue

        null_columns = [
            column
            for column, column_rules in column_schema.items()
            if column_rules.get("not_null") and df[column].isna().any()
        ]

        if null_columns:
            errors["null_values"].append(
                {
                    "table": table_name,
                    "columns": null_columns,
                }
            )

        for unique_columns in table_schema.get("unique", []):
            mask = df[unique_columns].duplicated()

            if mask.any():
                errors["duplicate_values"].append(
                    {
                        "table": table_name,
                        "columns": unique_columns,
                    }
                )

    if errors:
        raise RuntimeError(errors)
