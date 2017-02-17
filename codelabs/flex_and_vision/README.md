# Python Google Cloud Vision sample for Google App Engine Flexible Environment

This sample demonstrates how to use the [Google Cloud Vision API](https://cloud.google.com/vision/), [Google Cloud Storage](https://cloud.google.com/storage/), and [Google Cloud Datastore](https://cloud.google.com/datastore/) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Setup and Authentication

Create a new project with the [Google Cloud Platform console](https://console.cloud.google.com/).
Make a note of your project ID, which may be different than your project name.

Make sure to [Enable Billing](https://pantheon.corp.google.com/billing?debugUI=DEVELOPERS)
for your project.

Download the [Google Cloud SDK](https://cloud.google.com/sdk/docs/) to your
local machine. Alternatively, you could use the [Cloud Shell](https://cloud.google.com/shell/docs/quickstart), which comes with the Google Cloud SDK pre-installed.

Initialize the Google Cloud SDK:

    $ gcloud init

Create your App Engine application:

    $ gcloud app create

Enable the APIs:

    $ gcloud service-management enable vision.googleapis.com
    $ gcloud service-management enable storage-component.googleapis.com
    $ gcloud service-management enable datastore.googleapis.com

Create a Service Account and set the `GOOGLE_APPLICATION_CREDENTIALS`
environment variable, replacing `YOUR_PROJECT_ID` and `/absolute/path/to/your/`
with appropriate values.

    $ gcloud iam service-accounts keys create ~/key.json --iam-account \
    [YOUR_PROJECT_ID]@appspot.gserviceaccount.com
    $ export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your/key.json"

## Running locally

Create a virtual environment and install dependencies:

    $ virtualenv -p python3 env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Create a Cloud Storage bucket. It is recommended that you name it the same as
your project ID.

    $ gsutil mb gs://[YOUR_CLOUD_STORAGE_BUCKET]

Set the environment variable `CLOUD_STORAGE_BUCKET`:

    $ export CLOUD_STORAGE_BUCKET=[YOUR_CLOUD_STORAGE_BUCKET]

Start your application locally:

    $ python main.py

Visit `localhost:8080` to view your application running locally. Press `Control-C`
on your command line when you are finished.

When you are ready to leave your virtual environment:

    $ deactivate

## Deploying to App Engine

Open `app.yaml` and replace <your-cloud-storage-bucket> with the name of your
Cloud Storage bucket.

Deploy your application to App Engine using `gcloud`. Please note that this may
take several minutes.

    $ gcloud app deploy

Visit https://[YOUR_PROJECT_ID].appspot.com to view your deployed application.
