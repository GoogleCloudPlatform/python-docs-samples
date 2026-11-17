# Cloud Spanner GoogleSQL Samples

Python samples demonstrating GoogleSQL queries, partitioned [Spanner Data Boost](https://cloud.google.com/spanner/docs/databoost/databoost-overview) reads (`data_boost_enabled=True`), and connecting to the [Cloud Spanner Emulator](https://cloud.google.com/spanner/docs/emulator).

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
   python src/spanner_googlesql/data_boost_partitioned_query.py \
       --instance-id "example-instance" \
       --database-id "example-db"
   ```

## Running Tests

Run unit tests offline:

```sh
pip install -r requirements-test.txt
pytest tests
```
