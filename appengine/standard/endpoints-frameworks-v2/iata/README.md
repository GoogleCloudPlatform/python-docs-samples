## Endpoints Frameworks v2 Python Sample (Airport Information Edition)

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/endpoints-frameworks-v2/echo/README.md

This demonstrates how to use Google Cloud Endpoints Frameworks v2 on Google App Engine Standard Environment using Python.

## Setup

Create a `lib` directory in which to install the Endpoints Frameworks v2 library. For more info, see [Installing a library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).

Install the Endpoints Frameworks v2 library:

    $ pip install -t lib -r requirements.txt

## Deploying to Google App Engine

Generate an OpenAPI file by running: `python lib/endpoints/endpointscfg.py get_openapi_spec main.IataApi --hostname [YOUR-PROJECT-ID].appspot.com`

Remember to replace [YOUR-PROJECT-ID] with your project ID.

Deploy the generated service spec to Google Cloud Service Management: `gcloud endpoints services deploy iatav1openapi.json`

The command returns several lines of information, including a line similar to the following:

   Service Configuration [2016-08-01r0] uploaded for service "[YOUR-PROJECT-ID].appspot.com"

Open the `app.yaml` file and in the `env_variables` section, replace [YOUR-PROJECT-ID] in `[YOUR-PROJECT-ID].appspot.com` with your project ID. This is your Endpoints service name. Then replace `2016-08-01r0` with your uploaded service management configuration.

Then, deploy the sample using `gcloud`:

    $ gcloud app deploy

Once deployed, you can access the application at https://your-service.appspot.com
