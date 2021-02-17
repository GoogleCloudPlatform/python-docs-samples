# Python Google Cloud Pub/Sub sample for Google App Engine Standard Environment

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/pubsub/README.md

This demonstrates how to send and receive messages using [Google Cloud Pub/Sub](https://cloud.google.com/pubsub) on [Google App Engine Standard Environment](https://cloud.google.com/appengine/docs/standard/) for
Python 2.7 or for Python 3. See instructions below for deploying in either
of those two environments.

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Enable the Cloud Pub/Sub API in the [Google Developers Console](https://console.developers.google.com/project/_/apiui/apiview/pubsub/overview).

1. Allow Cloud Pub/Sub to create authentication tokens in your project. Note
that this command uses both your-project-id (the name you gave the project) and
your-project-number (the numeric identifier automatically assigned to your
project) in separate places.

        $ gcloud projects add-iam-policy-binding [your-project-id] \
            --member=serviceAccount:service-[your-project-number]@gcp-sa-pubsub.iam.gserviceaccount.com \
            --role=roles/iam.serviceAccountTokenCreator

1. Create a topic and subscription. The `--push-auth-service-account` flag activates the Pub/Sub push functionality for Authentication and Authorization. Pub/Sub messages pushed to your endpoint will carry the identity of this service account. You may use an existing service account or create a new one. The `--push-auth-token-audience` flag is optional; if set, remember to modify the audience field check in `main.py`.

        $ gcloud pubsub topics create [your-topic-name]
        $ gcloud beta pubsub subscriptions create [your-subscription-name] \
            --topic=[your-topic-name] \
            --push-endpoint=\
                https://[your-app-id].appspot.com/push-handlers/receive_messages?token=[your-token] \
            --ack-deadline=30 \
            --push-auth-service-account=[your-service-account] \
            --push-auth-token-audience=example.com

1. Update the environment variables in ``app.yaml`` for Python 3, or ``app27.yaml`` for Python 2.7.

## Running locally

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

Install dependencies, preferably with a virtualenv:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Then set environment variables before starting your application:

    $ export GOOGLE_CLOUD_PROJECT=[your-project-name]
    $ export PUBSUB_VERIFICATION_TOKEN=[your-verification-token]
    $ export PUBSUB_TOPIC=[your-topic]
    $ python main.py

### Simulating push notifications

The application can send messages locally, but it is not able to receive push messages locally. You can, however, simulate a push message by making an HTTP request to the local push notification endpoint. There is an included ``sample_message.json``. You can use
``curl`` or [httpie](https://github.com/jkbrzt/httpie) to POST this:

    $ curl -i --data @sample_message.json "localhost:8080/push-handlers/receive_messages?token=[your-token]"

Or

    $ http POST ":8080/push-handlers/receive_messages?token=[your-token]" < sample_message.json

Response:

    HTTP/1.0 400 BAD REQUEST
    Content-Type: text/html; charset=utf-8
    Content-Length: 58
    Server: Werkzeug/0.15.2 Python/3.7.3
    Date: Sat, 06 Apr 2019 04:56:12 GMT

    Invalid token: 'NoneType' object has no attribute 'split'

The simulated push request fails because it does not have a Cloud Pub/Sub-generated JWT in the "Authorization" header.

## Running on App Engine

Note: Not all the files in the current directory are needed to run your code on App Engine. Specifically, `main_test.py` and the `data` directory, which contains a mocked private key file and a mocked public certs file, are for testing purposes only. They SHOULD NOT be included when deploying your app. When your app is up and running, Cloud Pub/Sub's push servers create tokens using a private key, then the Google Auth Python library takes care of verifying and decoding the token using Google's public certs, to confirm that the push requests indeed come from Cloud Pub/Sub.

In the current directory, deploy using `gcloud`. For Python 2.7 you must first
install the required libraries in the `lib` folder:

    $ pip -t lib -r requirements.txt
    $ gcloud app deploy app27.yaml

For Python 3, you can simply run the deploy command:

    $ gcloud app deploy app.yaml

You can now access the application using the `gcloud app browse` command. You
can use the form to submit messages, but it's non-deterministic which instance
of your application will receive the notification. You can send multiple 
messages and refresh the page to see the received message.
