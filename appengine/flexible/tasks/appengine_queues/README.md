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

The samples require a Python environment with
[pip](https://pypi.python.org/pypi/pip) installed.
[virtualenv](https://virtualenv.readthedocs.org/en/latest/) is also recommended.

All samples require a Google Cloud Project whitelisted for the Cloud Tasks API.

* Enable the Cloud Tasks API
* Enable the Cloud Datastore API (used to demonstrate storing payloads)

To create a project and enable the API, go to the [Google Developers
Console](https://console.developer.google.com). You must also create an API key.
This can be done under API Manager -> Credentials.

To install the Python application dependencies, run the following commands:

    * pip install -r requirements.txt

## Authentication

To set up authentication locally, download the
[Cloud SDK](https://cloud.google.com/sdk), and run

    gcloud auth application-default login

On App Engine, authentication credentials will be automatically detected.

On Compute Engine and Container Engine, authenticatino credentials will be
automatically detected, but the instances must have been created with the
necessary scopes.

In any other environment, for example Compute Engine instance without the
necessary scopes, you should set `GOOGLE_APPLICATION_CREDENTIALS` environment
variable to a JSON key file for a service account.

See the [authentication guide](https://cloud.google.com/docs/authentication)
for more information.

## Creating a queue

Queues can not currently be created by the API. To create a queue using the
Cloud SDK, use the provided queue.yaml:

    gcloud app deploy queue.yaml

## Deploying the App Engine app

First, vendor the dependencies into the project:

    pip install -r requirements.txt

Next, deploy the App Engine app

    gcloud app deploy

Verify the index page is serving:

    gcloud app browse

The App Engine app serves as a target for the push requests. It has an
endpoint `/set_payload` that that stores the payload from the HTTP POST data in
Cloud Datastore. The payload can be accessed in your browser at the
 `/get_payload` endpoint with a GET request.

## Running the Samples

The project ID must be specified either as a command line argument using
`--project-id`, or by editing `DEFAULT_PROJECT_ID` within `task_snippets.py`.

Set the environment variables:

    export PROJECT_ID=my-project-id
    export LOCATION_ID=us-central1
    export QUEUE_ID=my-appengine-queue # From queue.yaml

View all queues:

     python app_engine_queue_snippets.py --api_key=$API_KEY list-queues --project_id=$PROJECT_ID --location_id=$LOCATION_ID

Set the queue name as an environment variable:

    export QUEUE_NAME=projects/$PROJECT_ID/locations/$LOCATION_ID/queues/$QUEUE_ID

Create a task, targeted at the `set_payload` endpoint with a payload specified:

   python app_engine_queue_snippets.py --api_key=$API_KEY create-task --queue_name=$QUEUE_NAME --payload=hello

Now view that the payload was received and verify the count and payload:

    http://your-app-id.appspot.com/get_payload

Create a task that will be scheduled for a few seconds in the future using
the `--in_seconds` flag:

    python app_engine_queue_snippets.py --api_key=$API_KEY create-task --queue_name=$QUEUE_NAME --payload=hello --in_seconds=30

Since `--in_seconds` was set to 30, it will take 30 seconds for the new
payload to be pushed to the `/get_payload` endpoint, which can then be viewed at:

    http://your-app-id.appspot.com/get_payload

It might also be helpful to view the request logs of your App Engine app:

    https://console.cloud.google.com/logs

## Testing the Samples

Install the testing dependencies:

    pip install -r requirements-test.txt

Run pytest:

    pytest
