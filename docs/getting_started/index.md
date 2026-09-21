# Getting Started

This package makes it easy to retrieve data from, and interact with Relatics. The main use cases of the package are:

- Single report part extraction.
- Element extraction.

## Single report part extraction
In order to do single report part extraction and transformation using this package the following code can be used:

```python
from relatics_toolkit import RelaticsClient, parse_xml

# Retrieve XML from relatics webservice
client = RelaticsClient(client_id, client_secret, environment)
result = client.get_request(workspace_id, operation)

# Parse resulting XML
parsed_df = parse_xml(result, "ReportPart")
```

Now parsed_df is a pandas DataFrame and can be used for downstream applications.

!!! note
    Relatics doesn't include parts of a report if they are empty. If for example a property is added in a report part, but is never used in Relatics, the corresponding column will not show up in the webservice and therefore not in the DataFrame.

## Element extraction
To extract all Element data a very specific Relatics report needs to be constructed, more about this on the next page.

The `extract_element_tables` function will do the following:

- Produce a table with a column for the Name, Description, RichText and GUID attributes of the Element, a column for all its properties and a column for all relations with a to-one cardinality.
- Produce a link table for each relation the element has to other elements with to-many cardinality. The link table will only have the *r1_element_guid*, *r2_element_guid* and *workspace_guid*

!!! example
    If a **person** element has a to-many relation with the **device** element. The link table will be called **person_device** and will contain the columns: *person_guid*, *device_guid* and *workspace_guid*

- Combine all these tables into a dictionary and return it.

For a more detailed explanation on how to install and set up Relatics follow the next pages in this getting started!