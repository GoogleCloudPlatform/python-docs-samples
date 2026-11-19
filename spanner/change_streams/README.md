# Cloud Spanner Change Streams Samples

Python samples demonstrating Cloud Spanner change stream DDL creation, transaction-level write exclusion, and `READ_<ChangeStream>` TVF queries.

## Setup

1. Create and activate a Python 3.13+ virtual environment:

   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Running Tests

Run unit tests offline:

```sh
pip install -r requirements-test.txt
pytest tests
```
