# Google Developer Knowledge API Python Samples

This directory contains Python code samples demonstrating how to use the [Google Developer Knowledge API](https://developers.google.com/knowledge) client library (`google-developer-knowledge`).

## Setup

1. Enable the Developer Knowledge API on your Google Cloud project:
   ```bash
   gcloud services enable developerknowledge.googleapis.com
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Samples

* **[Search Document Chunks](search_document_chunks.py)**: Search public developer documentation chunks by query (`developerknowledge_search_document_chunks`).
* **[Get Document](get_document.py)**: Retrieve a single documentation page with full markdown content (`developerknowledge_get_document`).
* **[Batch Get Documents](batch_get_documents.py)**: Fetch multiple documentation pages in one call (`developerknowledge_batch_get_documents`).
* **[Answer Query](answer_query.py)**: Get a grounded, cited answer to a technical question (`developerknowledge_answer_query`).

## Running Tests

```bash
pytest
```
