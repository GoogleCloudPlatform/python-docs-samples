# Google Cloud Endpoints & Python

This sample demonstrates how to use Google Cloud Endpoints using Python.

For a complete walkthrough showing how to run this sample in different
environments, see the
[Google Cloud Endpoints Quickstarts](https://cloud.google.com/endpoints/docs/quickstarts).

This sample consists of two parts:

1. The backend
2. The clients

## Running locally

### Running the backend

Install all the dependencies:
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Run the application:
```bash
$ python main.py
```

### Using the echo client

With the app running locally, you can execute the simple echo client using:
```bash
$ python clients/echo-client.py http://localhost:8080 APIKEY helloworld
```

The `APIKEY` doesn't matter as the endpoint proxy is not running to do authentication.

## Deploying to Production

See the
[Google Cloud Endpoints Quickstarts](https://cloud.google.com/endpoints/docs/quickstarts).

### Using the echo client

With the project deployed, you'll need to create an API key to access the API.

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'API Key'.
4. Choose 'Server Key'

With the API key, you can use the echo client to access the API:
```bash
$ python clients/echo-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY helloworld
```

### Using the JWT client (with key file)

The JWT client demonstrates how to use a service account to authenticate to endpoints with the service account's private key file. To use the client, you'll need both an API key (as described in the echo client section) and a service account. To create a service account:

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'Service account key'.
4. In the 'Select service account' dropdown, select 'Create new service account'.
5. Choose 'JSON' for the key type.

To use the service account for authentication:

1. Update the `google_jwt`'s `x-google-jwks_uri` in `openapi.yaml` with your service account's email address.
2. Redeploy your application.

Now you can use the JWT client to make requests to the API:
```bash
$ python clients/google-jwt-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY /path/to/service-account.json
```

### Using the ID Token client (with key file)

The ID Token client demonstrates how to use user credentials to authenticate to endpoints. To use the client, you'll need both an API key (as described in the echo client section) and a OAuth2 client ID. To create a client ID:

1. Open the Credentials page of the API Manager in the [Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Click 'Create credentials'.
3. Select 'OAuth client ID'.
4. Choose 'Other' for the application type.

To use the client ID for authentication:

1. Update the `google_id_token`'s `x-google-audiences` in `openapi.yaml`with your client ID.
2. Redeploy your application.

Now you can use the client ID to make requests to the API:
```bash
$ python clients/google-id-token-client.py https://YOUR-PROJECT-ID.appspot.com YOUR-API-KEY /path/to/client-id.json
```

### Using the App Engine default service account client (no key file needed)

The App Engine default service account client demonstrates how to use the Google App Engine default service account to authenticate to endpoints.
We refer to the project that serves API requests as the server project. You also need to create a client project in the [Cloud Console](https://console.cloud.google.com). The client project is running Google App Engine standard application.

To use the App Engine default service account for authentication:

1. Update the `gae_default_service_account`'s `x-google-issuer` and `x-google-jwks_uri` in `openapi.yaml` with your client project ID.
2. Redeploy your server application.
3. Update clients/service_to_service_gae_default/main.py, replace 'YOUR-CLIENT-PROJECT-ID' and 'YOUR-SERVER-PROJECT-ID' with your client project ID and your server project ID.
4. Upload your application to Google App Engine by invoking the following command. Note that you need to provide project ID in the command because there are two projects (server and client projects) here and gcloud needs to know which project to pick.
```bash
$ gcloud app deploy app.yaml --project=YOUR-CLIENT-PROJECT-ID
```

Your client app is now deployed at https://YOUR-CLIENT-PROJECT-ID.appspot.com. When you access https://YOUR-CLIENT-PROJECT-ID.appspot.com, your client calls your server project API using
the client's service account.

### Using the service account client (no key file needed)

The service account client demonstrates how to use a non-default service account to authenticate to endpoints.
We refer to the project that serves API requests as the server project. You also need to create a client project in the [Cloud Console](https://console.cloud.google.com).
The client project is running Google App Engine standard application.

In the example, we use Google Cloud Identity and Access Management (IAM) API to create a JSON Web Token (JWT) for a service account, and use it to call an Endpoints API.

To use the client, you will need to enable "Service Account Actor" role for App Engine default service account:

1. Go to [IAM page](https://console.cloud.google.com/iam-admin/iam) of your client project.
2. For App Engine default service account, from “Role(s)” drop-down menu, select “Project”-“Service Account Actor”, and Save.

You also need to install Google API python library because the client code (main.py) uses googleapiclient,
which is a python library that needs to be uploaded to App Engine with your application code. After you run "pip install -t lib -r requirements",
Google API python client library should have already been installed under 'lib' directory. Additional information can be found
[here](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#requesting_a_library).

To use the client for authentication:

1. Update the `google_service_account`'s `x-google-issuer` and `x-google-jwks_uri` in `openapi.yaml` with your service account email.
2. Redeploy your server application.
3. Update clients/service_to_service_non_default/main.py by replacing 'YOUR-SERVICE-ACCOUNT-EMAIL', 'YOUR-SERVER-PROJECT-ID' and 'YOUR-CLIENT-PROJECT-ID'
with your service account email, your server project ID, and your client project ID, respectively.
4. Upload your application to Google App Engine by invoking the following command. Note that you need to provide project ID in the command because there are two projects (server and client projects) here and gcloud needs to know which project to pick.
```bash
$ gcloud app deploy app.yaml --project=YOUR-CLIENT-PROJECT-ID
```

Your client app is now deployed at https://YOUR-CLIENT-PROJECT-ID.appspot.com. When you access https://YOUR-CLIENT-PROJECT-ID.appspot.com, your client calls your server project API using
the client's service account.

### Using the ID token client (no key file needed)

This example demonstrates how to authenticate to endpoints from Google App Engine default service account using Google ID token.
In the example, we first create a JSON Web Token (JWT) using the App Engine default service account. We then request a Google
ID token using the JWT, and call an Endpoints API using the Google ID token.

We refer to the project that serves API requests as the server project. You also need to create a client project in the [Cloud Console](https://console.cloud.google.com).
The client project is running Google App Engine standard application.

To use the client for authentication:

1. Update clients/service_to_service_google_id_token/main.py, replace 'YOUR-CLIENT-PROJECT-ID' and 'YOUR-SERVER-PROJECT-ID' with your client project ID and your server project ID.
2. Upload your application to Google App Engine by invoking the following command. Note that you need to provide project ID in the command because there are two projects (server and client projects) here and gcloud needs to know which project to pick.
```bash
$ gcloud app deploy app.yaml --project=YOUR-CLIENT-PROJECT-ID
```

Your client app is now deployed at https://YOUR-CLIENT-PROJECT-ID.appspot.com. When you access https://YOUR-CLIENT-PROJECT-ID.appspot.com, your client calls your server project API from
the client's service account using Google ID token.
