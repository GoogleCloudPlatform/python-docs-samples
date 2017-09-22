# Google Cloud Tasks App Engine Queue Samples

Sample command-line program for interacting with the Cloud Tasks API
using App Engine queues.

App Engine queues push tasks to an App Engine HTTP target. This directory
contains both the App Engine app to deploy, as well as the snippets to run
locally to push tasks to it, which could also be called on App Engine.

`app_engine_queue_snippets.py` is a simple command-line program to create tasks
to be pushed to the App Engine app.

`main.py` is the main App Engine app. This app serves as an endpoint to receive
App Engine task attempts.

`app.yaml` configures the App Engine app.


## Prerequisites to run locally:

Please refer to [Setting Up a Python Development Environment](https://cloud.google.com/python/setup).

## Authentication

To set up authentication, please refer to our
[authentication getting started guide](https://cloud.google.com/docs/authentication/getting-started).

## Creating a queue

To create a queue using the Cloud SDK, use the following gcloud command:

    gcloud alpha tasks queues create-app-engine-queue my-appengine-queue

Note: A newly created queue will route to the default App Engine service and
version unless configured to do otherwise. Read the online help for the
`create-app-engine-queue` or the `update-app-engine-queue` commands to learn
about routing overrides for App Engine queues.

## Deploying the App Engine app

Deploy the App Engine app with gcloud:

    gcloud app deploy

Verify the index page is serving:

    gcloud app browse

The App Engine app serves as a target for the push requests. It has an
endpoint `/log_payload` that reads the payload (i.e., the request body) of the
HTTP POST request and logs it. The log output can be viewed with:

    gcloud app logs read

## Running the Samples

Set environment variables:

First, your project ID:

    export PROJECT_ID=my-project-id

Then the queue ID, as specified at queue creation time. Queue IDs already
created can be listed with `gcloud alpha tasks queues list`.

    export QUEUE_ID=my-appengine-queue

And finally the location ID, which can be discovered with
`gcloud alpha tasks queues describe $QUEUE_ID`, with the location embedded in
the "name" value (for instance, if the name is
"projects/my-project/locations/us-central1/queues/my-appengine-queue", then the
location is "us-central1").

    export LOCATION_ID=us-central1

Create a task, targeted at the `log_payload` endpoint, with a payload specified:

   python create_app_engine_queue_task.py --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID --payload=hello

Now view that the payload was received and verify the payload:

    gcloud app logs read

Create a task that will be scheduled for a time in the future using the
`--in_seconds` flag:

    python create_app_engine_queue_task.py --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID --payload=hello --in_seconds=30
