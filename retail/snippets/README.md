# Vertex AI Search for commerce Samples

This directory contains Python samples for [Vertex AI Search for commerce](https://cloud.google.com/retail/docs/search-basic#search).

## Prerequisites

To run these samples, you must have:

1.  **A Google Cloud Project** with the [Vertex AI Search for commerce API](https://console.cloud.google.com/apis/library/retail.googleapis.com) enabled.
2.  **Vertex AI Search for commerce** set up with a valid catalog and serving configuration (placement).
3.  **Authentication**: These samples use [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc).
    - If running locally, you can set up ADC by running:
      ```bash
      gcloud auth application-default login
      ```
4.  **IAM Roles**: The service account or user running the samples needs the `roles/retail.viewer` (Retail Viewer) role or higher.

## Samples

- **[search_request.py](search_request.py)**: Basic search request showing both text search and browse search (using categories).
- **[search_pagination.py](search_pagination.py)**: Shows how to use `next_page_token` to paginate through search results.
- **[search_offset.py](search_offset.py)**: Shows how to use `offset` to skip a specified number of results.

## Documentation

For more information, see the [Vertex AI Search for commerce documentation](https://docs.cloud.google.com/retail/docs/search-basic#search).
