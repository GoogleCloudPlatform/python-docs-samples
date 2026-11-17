# Cloud Spanner DML Samples

Python samples demonstrating GoogleSQL DML statements, DML `THEN RETURN` queries, and `last_statement=True` transaction optimizations in Cloud Spanner.

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
