# Relatics Toolkit

Welcome to the Relatics Toolkit documentation. This package provides a comprehensive solution for extracting, parsing, and transforming data from Relatics, enabling seamless integration with downstream applications and database storage.

## Overview

The Relatics Toolkit is designed to simplify interactions with the Relatics DataExchange API, offering:

- **Authentication**: OAuth 2.0 token-based authentication support
- **Report Extraction**: Extraction of Relatics reports exposed in webservices
- **XML Processing**: Parsing of complex nested XML structures
- **Element Extraction**: Extraction of Relatics elements into normalized relational tables

## Key Features

#### Single Report Part Extraction

For extracting specific report parts, you can use the `RelaticsClient` class along with the `parse_xml` function to retrieve and parse XML data exposed in a Relatics webservice.

#### Element Extraction

To extract the all data related to a selection of Elements, use the `extract_element_tables` function:

- Retrieves elements using their `ElementID`
- Extracts element information including `Name`, `Description`, `RichText`, and `GUID`
- Extracts all user defined properties of the Element
- Created reference columns for all to-one relations of the Element
- Creates appropriate link tables for to-many relationships of the Element
- Combines all data into a structured dictionary format with table names as keys and pandas DataFrames as values

## Core Components

### RelaticsClient
The `RelaticsClient` class handles authentication and API requests to the Relatics DataExchange API.

### parse_xml
The `parse_xml` function parses deeply nested XML structures returned by Relatics into structured pandas DataFrames.

### extract_element_tables
The `extract_element_tables` function orchestrates the complete extraction, parsing, schema validation, and transformation for Relatics Element data into database-ready pandas DataFrames.

## Getting Started

To get started with the Relatics Connector, refer to the [Getting Started](getting_started/index.md) guide which provides detailed instructions on setting up your environment and running basic extractions.