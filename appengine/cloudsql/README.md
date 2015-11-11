# Using Cloud SQL from Google App Engine

This is an example program showing how to use the native MySQL connections from Google App Engine to [Google Cloud SQL](https://cloud.google.com/sql).

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## Setup

1. You will need to create a [Cloud SQL instance](https://cloud.google.com/sql/docs/create-instance).

2. Edit the `CLOUDSQL_INSTANCE` and `CLOUDSQL_PROJECT` values in `main.py`.

3. To run locally, you will need to be running a local instance of MySQL. You may need to update the connection code in `main.py` with the appropriate local username and password.
