# Google Cloud Endpoints & App Engine Flexible Environment & Python

This sample demonstrates how to use Google Cloud Endpoints on Google App Engine Flexible Environment using Python.

This sample consists of two parts:

1. The backend
2. The clients

## Running locally

### Running the backend

For more info on running Flexible applications locally, see [the getting started documentation](https://cloud.google.com/appengine/docs/managed-vms/python/hello-world).

Install all the dependencies:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Run the application:

    $ python main.py

In your web browser, go to the following address: http://localhost:8080.

### Using the echo client

With the app running locally, you can execute the simple echo client using:

    $ python clients/echo-client.py http://localhost:8080 APIKEY helloworld

The `APIKEY` doesn't matter as the endpoint proxy is not running to do authentication.

## Deploying to Google App Engine

Open the `swagger.yaml` file and in the `host` property, replace
`YOUR-PROJECT-ID` with your project's ID.

Then, deploy the sample using `gcloud`:

    gcloud preview app deploy app.yaml

Once deployed, you can access the application at https://YOUR-PROJECT-ID.appspot.com/.

### Using the echo client

With the project deployed, you'll need to create an API key to access the API.

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'API Key'.
4. Choose 'Server Key'

With the API key, you can use the echo client to access the API:

    $ python clients/echo-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY

### Using the JWT client.

The JWT client demonstrates how to use service accounts to authenticate to endpoints. To use the client, you'll need both an API key (as described in the echo client section) and a service account. To create a service account:

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'Service account key'.
4. In the 'Select service account' dropdown, select 'Create new service account'.
5. Choose 'JSON' for the key type.

To use the service account for authentication:

1. Update the `google_jwt`'s `x-jwks_uri` in `swagger.yaml` with your service account's email address.
2. Redeploy your application.

Now you can use the JWT client to make requests to the API:

    $ python clients/google-jwt-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY /path/to/service-account.json

### Using the ID Token client.

The ID Token client demonstrates how to use user credentials to authenticate to endpoints. To use the client, you'll need both an API key (as described in the echo client section) and a OAuth2 client ID. To create a client ID:

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'OAuth client ID'.
4. Choose 'Other' for the application type.

To use the client ID for authentication:

1. Update the `/auth/info/googleidtoken`'s `audiences` in `swagger.yaml` with your client ID.
2. Redeploy your application.

Now you can use the client ID to make requests to the API:

    $ python clients/google-id-token-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY /path/to/client-id.json
