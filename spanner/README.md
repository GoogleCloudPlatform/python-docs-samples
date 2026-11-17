# Cloud Spanner Python Samples

Python samples for [Cloud Spanner](https://cloud.google.com/spanner/docs), organized by functional area:

- [`googlesql/`](googlesql/): GoogleSQL queries, partitioned Data Boost reads, and local Cloud Spanner Emulator connections.
- [`search_and_ai/`](search_and_ai/): Vector search (exact kNN and approximate ANN with `VECTOR INDEX`), full-text search (`SEARCH INDEX`), hybrid Reciprocal Rank Fusion (RRF), and Vertex AI `ML.PREDICT` embeddings and generative AI queries.
- [`graph/`](graph/): Spanner Graph (`GRAPH_TABLE`) vector similarity and full-text search queries.
- [`transactions/`](transactions/): Transaction isolation levels and pessimistic row locking (`SELECT ... FOR UPDATE` under `REPEATABLE_READ`).

Each directory is a self-contained Python 3.13+ sample package with pinned `requirements.txt` dependencies and `pytest` unit and live integration tests under `tests/`.
