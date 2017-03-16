## Endpoints Frameworks v2 Python Sample

This demonstrates how to use Google Cloud Endpoints Frameworks v2 on Google App Engine Standard Environment using Python.

## Setup

Create a `lib` directory in which to install the Endpoints Frameworks v2 library. For more info, see [Installing a library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).

Install the Endpoints Frameworks v2 library:

    $ pip install -t lib -r requirements.txt

## Deploying to Google App Engine

Generate a swagger file by running: `python lib/endpoints/endpointscfg.py get_swagger_spec main.EchoApi --hostname echo-api.endpoints.[YOUR-PROJECT-ID].cloud.goog`

Remember to replace [YOUR-PROJECT-ID] with your project ID.

To set up OAuth2, replace `your-oauth-client-id.com` under `audiences` in the annotation for `get_user_email` with your OAuth2 client ID. If you want to use Google OAuth2 Playground, use `407408718192.apps.googleusercontent.com` as your audience. To generate a JWT, go to the following address: `https://developers.google.com/oauthplayground`.

Deploy the generated swagger spec to Google Cloud Service Management: `gcloud alpha service-management deploy echo-v1_swagger.json`

The command returns several lines of information, including a line similar to the following:

   Service Configuration [2016-08-01r0] uploaded for service "echo-api.endpoints.[YOUR-PROJECT-ID].cloud.goog"

Open the `app.yaml` file and in the `env_variables` section, replace [YOUR-PROJECT-ID] in `echo-api.endpoints.[YOUR-PROJECT-ID].cloud.goog` with your project ID. This is your Endpoints service name. Then replace `2016-08-01r0` with your uploaded service management configuration.

Then, deploy the sample using `gcloud`:

    $ gcloud app deploy

Once deployed, you can access the application at https://your-service.appspot.com

Note that local deployment with dev_appserver.py is not yet supported with
Endpoints Frameworks v2.
