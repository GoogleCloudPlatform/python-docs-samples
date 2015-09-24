# Using Cloud SQL from Google App Engine

This is an example program showing how to use the native MySQL connections from Google App Engine to Google Cloud SQL.

## Running the sample

1. Edit the `CLOUDSQL_INSTANCE` and `CLOUDSQL_PROJECT` values in `main.py`.

2. If you have a local MySQL instance, run the app locally:

        dev_appserver.py .

2. Upload the app: 

        appcfg.py update .
