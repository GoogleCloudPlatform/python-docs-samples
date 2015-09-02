## Google App Engine accessing BigQuery using OAuth2

This sample demonstrates [authenticating to BigQuery in App Engine using OAuth2](https://cloud.google.com/bigquery/authorization).

### Setup

* To install dependencies for this sample, run:

    $ pip install -t lib -r requirements.txt

* You must then update `main.py` and replace `<myproject_id>` with your project's
  id.
* You'll need a client id from your project - instructions
  [here](https://cloud-dot-devsite.googleplex.com/bigquery/authorization#clientsecrets).
  Once you've downloaded the client's json secret, copy it to the root directory
  of this project, and rename it to `client_secrets.json`.
* You can then run the sample on your development server:

    $ dev_appserver.py .
