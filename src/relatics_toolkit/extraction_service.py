import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal

import pandas as pd

from relatics_toolkit.ingestion.relatics_client import RelaticsClient
from relatics_toolkit.ingestion.xml_parser import parse_xml
from relatics_toolkit.processing.schema import SCHEMA
from relatics_toolkit.processing.transformer import create_element_tables
from relatics_toolkit.processing.validator import normalize_tables, validate_schema

logger = logging.getLogger(__name__)


def extract_element_tables(
    client: RelaticsClient,
    workspace_id: str,
    element_ids: list[str],
    operation: str,
    parallel: bool = False,
    max_workers: int | None = None,
    inline_relations: list[str] | None = None,
    errors: Literal['raise', 'ignore'] = 'raise',
) -> dict[str, pd.DataFrame]:
    """
    Extracts and transforms Relatics elements into normalized tables.

    For the specified workspace and element IDs, retrieves the
    corresponding Relatics XML payloads, validates the extracted schema,
    normalizes the resulting tables, and applies business transformations.

    Processing can be executed sequentially or in parallel.

    Args:
        client: Configured Relatics API client.
        workspace_id: Workspace ID containing the elements that should
            be extracted.
        element_ids: Element IDs that should be extracted from the
            workspace.
        operation: Relatics operation name used to retrieve the
            element data.
        parallel: Whether element extraction should be executed in
            parallel.
        max_workers: Maximum number of worker threads used when
            parallel is True. If None, the ThreadPoolExecutor
            default is used.
        inline_relations: Relation names of relations to R2 elements
            whose values should be materialized directly in the
            resulting element tables (must be to-one relations).
        errors: either set to 'raise' or 'ignore' changes the way
            the function handles errors in the extraction process.
            'raise' fails the entire extraction if a single element
            has errors. 'ignore' prints the exception to the console
            including element_id of the failed element and continues.

    Returns:
        Dictionary mapping table names to transformed pandas DataFrames.

    Raises:
        Exception: Any exception raised during retrieval, validation,
            normalization, or transformation of element data.
    """
    if type(errors) != str:
        raise TypeError(f"Argument errors should be of type: str but got {type(errors)}")

    if errors not in ['raise', 'ignore']:
        raise ValueError(f"Wrong string received for argument: errors. Expected 'raise' or 'ignore' but got {errors}")

    logger.info(
        "Starting extraction for %s elements in workspace %s (parallel=%s)",
        len(element_ids),
        workspace_id,
        parallel,
    )

    tables: dict[str, pd.DataFrame] = {}

    if parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(
                    _process_element,
                    element_id=element_id,
                    client=client,
                    workspace_id=workspace_id,
                    operation=operation,
                    inline_relations=inline_relations,
                ): element_id
                for element_id in element_ids
            }

            for future in as_completed(future_map):
                element_id = future_map[future]

                try:
                    _add_tables(tables, future.result())
                except Exception:
                    if errors == 'raise':
                        logger.error(
                            "Failed processing workspace_id=%s element_id=%s",
                            workspace_id,
                            element_id,
                        )
                        raise
                    elif errors == 'ignore':
                        logger.exception(f"Failed processing workspace_id={workspace_id} element_id={element_id}. Skipping...")
    else:
        for element_id in element_ids:
            try:
                _add_tables(
                    tables,
                    _process_element(
                        element_id=element_id,
                        client=client,
                        workspace_id=workspace_id,
                        operation=operation,
                        inline_relations=inline_relations,
                    ),
                )
            except Exception:
                if errors == 'raise':
                    logger.error(
                        "Failed processing workspace_id=%s element_id=%s",
                        workspace_id,
                        element_id,
                    )
                    raise
                elif errors == 'ignore':
                    logger.exception(f"Failed processing workspace_id={workspace_id} element_id={element_id}. Skipping...")

    logger.info(
        "Extraction completed successfully. Generated %s tables.",
        len(tables),
    )

    return tables


def _process_element(
    element_id: str,
    client: RelaticsClient,
    workspace_id: str,
    operation: str,
    schema: dict[str, dict] = SCHEMA,
    inline_relations: list[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Processes a Relatics element with its first order relations and properties.
    """
    parameters = {"ConfigurationOfRef": element_id}

    element_data = client.get_request(
        workspace_id=workspace_id,
        operation=operation,
        parameters=parameters,
    )

    tables = {table_name: parse_xml(element_data, table_name) for table_name in schema}
    normalized_tables = normalize_tables(tables=tables, schema=schema)
    validate_schema(tables=normalized_tables, schema=schema)
    transformed_tables = create_element_tables(
        tables=normalized_tables, inline_relations=inline_relations
    )

    for table in transformed_tables.values():
        table["workspace_guid"] = workspace_id

    return transformed_tables


def _add_tables(
    tables: dict[str, pd.DataFrame],
    element_tables: dict[str, pd.DataFrame],
) -> None:
    """Adds extracted tables and fails on duplicate table names."""
    for table_name, df in element_tables.items():
        if table_name in tables:
            raise RuntimeError(
                f"Duplicate table '{table_name}' produced during extraction."
            )

        tables[table_name] = df
