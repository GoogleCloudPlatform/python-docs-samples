# Cloud Spanner Queues Samples

Python samples demonstrating sending immediate and scheduled messages to Cloud Spanner queues, streaming `RECEIVE_<Queue>` rows, and acknowledging messages.

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
