# Cloud Spanner PostgreSQL-Dialect Samples

Python samples demonstrating PostgreSQL-dialect Spanner queries, DML `RETURNING` clauses, and `last_statement=True` transaction optimizations.

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
