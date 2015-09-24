## Google App Engine accessing BigQuery using OAuth2

This sample demonstrates [authenticating to BigQuery in App Engine using OAuth2](https://cloud.google.com/bigquery/authentication).

### Running the sample

1. To install dependencies for this sample, run:

        $ pip install -t lib -r requirements.txt

2. You must then update `main.py` and replace `<your-project-id>` with your project's
   ID.

3. You'll need a client id from your project - instructions
   [here](https://cloud.google.com/bigquery/authentication#clientsecrets).
   Once you've downloaded the client's json secret, copy it to the root directory
   of this project, and rename it to `client_secrets.json`.

3. You can then run the sample on your development server:
        
        $ dev_appserver.py .

   Or deploy the application:

        $ appcfg.py update .
