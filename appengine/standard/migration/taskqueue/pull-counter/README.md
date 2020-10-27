# App Engine Task Pull Queue Migration Sample

This sample replaces the
[App Engine Tasks Queue Pull Counter sample](../../../taskqueue/pull-counter)
that used the `taskqueue` library
available only in the App Engine Standard for Python 2.7 runtime.

The sample uses a
[Pub/Sub topic with a pull queue](https://cloud.google.com/pubsub/docs/pull)
as recommended in
[Migrating pull queues to Pub/Sub](https://cloud.google.com/appengine/docs/standard/python/taskqueue/pull/migrating-pull-queues)
to perform the same functions as the earlier, Task Queue sample.

The application has three functions:

* Viewing the home page will display a form to specify a task name, and add
  one more request for it. It will also show all requested tasks and their counts.

* Submitting the form on the home page will queue a task request.

* Requesting the page at `/_ah/start` will begin processing the queued tasks.
  This will run without responding to the request until the request is
  cancelled, or the request times out, which can be a significant amount
  of time.

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Enable the Cloud Pub/Sub API in the
[Google Developers Console](https://console.developers.google.com/project/_/apiui/apiview/pubsub/overview).

1. Check that Firestore is in Datastore mode in the
[Google Developers Console](https://console.cloud.google.com/datastore/welcome),
and select Datastore mode if it is not.

1. Select the project and account that will be used for locally run
[Google Cloud SDK](https://cloud.google.com/sdk) commands:

    $ gcloud init

1. Create a topic and subscription.

        $ gcloud pubsub topics create [YOUR_TOPIC_NAME]
        $ gcloud pubsub subscriptions create [YOUR_SUBSCRIPTION_NAME] \
            --topic=[YOUR_TOPIC_NAME]

1. Update the environment variables in ``app3.yaml`` for Python 3, or
``app.yaml`` for Python 2.7.

## Running locally

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk)
to provide authentication to use Google Cloud APIs. Initialize the SDK for
local commands if not already done.

    $ gcloud init

Install dependencies, preferably with a virtualenv:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Set environment variables before starting your application:

    $ export GOOGLE_CLOUD_PROJECT=[YOUR_PROJECT_NAME]
    $ export TOPIC=[YOUR_TOPIC_NAME]
    $ export SUBSCRIPTION=[YOUR_SUBSCRIPTION_NAME]

Run the application locally:

    $ python main.py

## Running on App Engine

In the current directory, edit the environment variables in `app.yaml` or
`app3.yaml`, depending on whether you are going to use Python 2.7 or
Python 3, and then deploy using `gcloud`.

For Python 2.7 you must first
install the required libraries in the `lib` folder:

    $ pip -t lib -r requirements.txt
    $ gcloud app deploy app.yaml

For Python 3, you only need to run the deploy command:

    $ gcloud app deploy app3.yaml

You can now access the application using the `gcloud app browse` command.
