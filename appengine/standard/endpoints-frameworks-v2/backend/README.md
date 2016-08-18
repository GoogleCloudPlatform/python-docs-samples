## Endpoints Frameworks v2 Python Sample

This demonstrates how to use Google Cloud Endpoints Frameworks v2 on Google App Engine Standard Environment using Python.

This sample consists of two parts:

1. The backend
2. The clients

## Running Locally

For more info on running Standard applications locally, see [the getting started documentation](https://cloud.google.com/appengine/docs/python/quickstart).

Create a `lib` directory in which to install the Endpoints Frameworks v2 library. For more info, see [Installing a library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).

Install the Endpoints Frameworks v2 library:

    $ mkdir lib
    $ pip install -t lib google-endpoints

Run the application:

    $ dev_appserver.py app.yaml

In your web browser, go to the following address: http://localhost:8080/\_ah/api/explorer

## Deploying to Google App Engine

Generate a swagger file by running: `endpointscfg.py get_swagger_spec main.EchoApi --hostname your-service.appspot.com`

To set up OAuth2, replace `your-oauth-client-id.com` under the `x-security` section in `echo-v1_swagger.json` with your OAuth2 client ID. If you want to use Google OAuth2 Playground, use `407408718192.apps.googleusercontent.com` as your audience. To generate a JWT, go to the following address: `https://developers.google.com/oauthplayground`.

Deploy the generated swagger spec to Google Cloud Service Management: `gcloud alpha service-management deploy echo-v1_swagger.json`

Open the `app.yaml` file and in the `env_variables` section, replace `your-service.appspot.com` with your service name, and `2016-08-01r0` with your uploaded service management configuration.

Then, deploy the sample using `gcloud`:

    $ gcloud beta app deploy

Once deployed, you can access the application at https://your-service.appspot.com
