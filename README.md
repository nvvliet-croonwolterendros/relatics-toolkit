[![Board Status](https://dev.azure.com/timsgravemade/1e99d87e-e84e-49f8-bd97-2752707e7af6/d4815894-bde2-4fb5-bfd0-506be7e228f4/_apis/work/boardbadge/0c3493b2-0e5a-478b-ad3d-51bbe2311940)](https://dev.azure.com/timsgravemade/1e99d87e-e84e-49f8-bd97-2752707e7af6/_boards/board/t/d4815894-bde2-4fb5-bfd0-506be7e228f4/Microsoft.RequirementCategory)
# Relatics Toolkit
[![Tests](https://github.com/nvvliet-croonwolterendros/relatics-extractor/actions/workflows/test.yml/badge.svg)](https://github.com/nvvliet-croonwolterendros/relatics-extractor/actions/workflows/test.yml)

A Python package for extracting, parsing, and transforming data from Relatics (a requirements management tool) into database-ready pandas DataFrames.

## Overview

The Relatics Toolkit is designed to streamline the process of extracting data from Relatics API endpoints and converting it into structured, normalized tables suitable for database storage. It handles complex relationships between entities, nested XML structures, and provides robust error handling throughout the extraction pipeline.

## Key Features

- **Authentication**: Implements OAuth 2.0 token-based authentication with Relatics API
- **Data Extraction**: Handles API calls to retrieve elements and their relationships
- **XML Parsing**: Parses deeply nested XML structures into pandas DataFrames
- **Schema Validation**: Validates data against predefined schemas and normalizes tables
- **Relationship Management**: Properly handles different relationship cardinalities:
  - :1 (one-to-one) relations are embedded in element tables  
  - :n (many-to-one) relations become link tables
- **Multithreading Support**: Uses ThreadPoolExecutor for faster processing of multiple elements
- **Error Handling**: Robust error handling with logging and failure tracking

## Documentation

Documentation can be found [here](https://nvvliet-croonwolterendros.github.io/relatics-toolkit/)

## License

MIT