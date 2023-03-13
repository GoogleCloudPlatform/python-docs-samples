# Python Google Cloud Pub/Sub sample for Google App Engine Flexible Environment

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible_python37_and_earlier/pubsub/README.md

This demonstrates how to send and receive messages using [Google Cloud Pub/Sub](https://cloud.google.com/pubsub) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Enable the Cloud Pub/Sub API in the [Google Developers Console](https://console.developers.google.com/project/_/apiui/apiview/pubsub/overview).

2. Create a topic and subscription.

        $ gcloud beta pubsub topics create [your-topic-name]
        $ gcloud beta pubsub subscriptions create [your-subscription-name] \
            --topic [your-topic-name] \
            --push-endpoint \
                https://[your-app-id].appspot.com/pubsub/push?token=[your-token] \
            --ack-deadline 30

3. Update the environment variables in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

Install dependencies, please follow https://cloud.google.com/python/docs/setup
to set up a Python development environment. Then run:

    $ pip install -r requirements.txt

Then set environment variables before starting your application:

    $ export PUBSUB_VERIFICATION_TOKEN=[your-verification-token]
    $ export PUBSUB_TOPIC=[your-topic]
    $ python main.py

### Simulating push notifications

The application can send messages locally, but it is not able to receive push messages locally. You can, however, simulate a push message by making an HTTP request to the local push notification endpoint. There is an included ``sample_message.json``. You can use
``curl`` or [httpie](https://github.com/jkbrzt/httpie) to POST this:

    $ curl -i --data @sample_message.json ":8080/pubsub/push?token=[your-token]"

Or

    $ http POST ":8080/pubsub/push?token=[your-token]" < sample_message.json

Response:

    HTTP/1.0 200 OK
    Content-Length: 2
    Content-Type: text/html; charset=utf-8
    Date: Mon, 10 Aug 2015 17:52:03 GMT
    Server: Werkzeug/0.10.4 Python/2.7.10

    OK

After the request completes, you can refresh ``localhost:8080`` and see the message in the list of received messages.

## Running on App Engine

Deploy using `gcloud`:

    gcloud app deploy app.yaml

You can now access the application at `https://your-app-id.appspot.com`. You can use the form to submit messages, but it's non-deterministic which instance of your application will receive the notification. You can send multiple messages and refresh the page to see the received message.
