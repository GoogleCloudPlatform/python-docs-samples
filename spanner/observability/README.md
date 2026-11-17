# Cloud Spanner Observability Samples

Python samples demonstrating Cloud Spanner OpenTelemetry client-side and end-to-end tracing, query execution latency histograms, and built-in metrics opt-out.

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
