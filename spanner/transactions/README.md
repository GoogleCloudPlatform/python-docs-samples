# Cloud Spanner Transaction Samples

Python samples demonstrating transaction isolation levels and pessimistic row locking (`SELECT ... FOR UPDATE` with `IsolationLevel.REPEATABLE_READ`) in [Cloud Spanner](https://cloud.google.com/spanner/docs/isolation-levels).

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

3. Set your Google Cloud project ID and run a sample:

   ```sh
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   python src/spanner_transactions/select_for_update.py \
       --instance-id "example-instance" \
       --database-id "example-db"
   ```

## Running Tests

Run unit tests offline:

```sh
pip install -r requirements-test.txt
pytest tests
```
