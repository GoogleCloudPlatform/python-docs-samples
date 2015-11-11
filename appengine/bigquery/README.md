# Google App Engine accessing BigQuery using OAuth2

This sample demonstrates [authenticating to BigQuery in App Engine using OAuth2](https://cloud.google.com/bigquery/authentication).

Refer to the [App Engine Samples README](../README.md) for information on how to run and deploy this sample.

## Setup

1. You'll need a client id for your project. Follow [these instructions](https://cloud.google.com/bigquery/authentication#clientsecrets). Once you've downloaded the client's json secret copy it into the sample directory and rename it to `client_secrets.json`.

2. Update `main.py` and replace `<your-project-id>` with your project's ID.
