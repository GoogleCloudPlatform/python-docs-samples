# Cloud Spanner Database Admin Samples

Python samples demonstrating Cloud Spanner database administration, online DDL
evolution, Customer-Managed Encryption Keys (CMEK), secondary indexes,
bit-reversed sequences, pre-splitting, and fine-grained access control (FGAC).

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
