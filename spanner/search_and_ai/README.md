# Cloud Spanner Search & AI Samples

Python samples demonstrating vector search (`COSINE_DISTANCE`, `APPROX_COSINE_DISTANCE`, and `VECTOR INDEX`), full-text search (`SEARCH`, `SCORE`, and `SEARCH INDEX`), hybrid Reciprocal Rank Fusion (RRF), and Vertex AI `ML.PREDICT` inference in [Cloud Spanner](https://cloud.google.com/spanner/docs).

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
   python src/spanner_search_and_ai/vector_search_knn.py \
       --instance-id "example-instance" \
       --database-id "example-db"
   ```

## Running Tests

Run unit tests offline:

```sh
pip install -r requirements-test.txt
pytest tests
```
