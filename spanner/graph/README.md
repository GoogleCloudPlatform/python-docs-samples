# Cloud Spanner Graph Samples

Python samples demonstrating [Spanner Graph](https://cloud.google.com/spanner/docs/graph/overview) (`GRAPH_TABLE`) queries combined with vector similarity (`COSINE_DISTANCE`) and full-text search (`SEARCH` and `SCORE`).

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
   python src/spanner_graph/graph_vector_search.py \
       --instance-id "example-instance" \
       --database-id "example-db"
   ```

## Running Tests

Run unit tests offline:

```sh
pip install -r requirements-test.txt
pytest tests
```
