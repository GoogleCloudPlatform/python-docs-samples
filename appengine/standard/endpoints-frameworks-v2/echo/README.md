## Endpoints Frameworks v2 Python Sample

This demonstrates how to use Google Cloud Endpoints Frameworks v2 on Google App Engine Standard Environment using Python.

## Setup

Create a `lib` directory in which to install the Endpoints Frameworks v2 library. For more info, see [Installing a library](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).

Install the Endpoints Frameworks v2 library:

    $ mkdir lib
    $ pip install -t lib google-endpoints

## Running Locally

For more info on running Standard applications locally, see [the getting started documentation](https://cloud.google.com/appengine/docs/python/quickstart).

Run the application:

    $ dev_appserver.py app.yaml

In your web browser, go to the following address: http://localhost:8080/\_ah/api/explorer

## Deploying to Google App Engine

Deploy the sample using `gcloud`:

    $ gcloud beta app deploy

Once deployed, you can access the application at https://your-service.appspot.com
