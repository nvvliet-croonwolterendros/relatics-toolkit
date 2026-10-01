# Relatics Client API Reference

Overview of the `RelaticsClient` class and associated custom exceptions for interacting with the Relatics DataExchange API.
This page includes documentation to execute a POST request and upload data to relatics. More information on the Relatics SOAP envelope can be found on the [Relatics 5 Knowledge Base](https://kb.relaticsonline.com/published//ShowObject.aspx?Key=644f0ded-2d55-e411-93f4-000af753dd5b)


## Client

::: relatics_toolkit.RelaticsClient
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3
      merge_init_into_class: true

## Exceptions

::: relatics_toolkit.ingestion.relatics_client.TokenRequestError
    options:
      show_root_heading: true
      heading_level: 3

::: relatics_toolkit.ingestion.relatics_client.APIRequestError
    options:
      show_root_heading: true
      heading_level: 3

::: relatics_toolkit.ingestion.relatics_client.XMLParseError
    options:
      show_root_heading: true
      heading_level: 3