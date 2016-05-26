# Python websockets sample for Google App Engine Flexible Environment

This sample demonstrates how to use websockets on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Setup

Before you can run or deploy the sample, you will need to create a new firewall rule to allow traffic on port 65080. This port will be used for websocket connections. You can do this with the [Google Cloud SDK](https://cloud.google.com/sdk) with the following command:

    $ gcloud compute firewall-rules create default-allow-websockets \
        --allow tcp:65080 \
        --target-tags websocket \
        --description "Allow websocket traffic on port 65080"

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn -b 127.0.0.1:8080 -b 127.0.0.1:65080 -k flask_sockets.worker main:app

## Python 3 Compatibility Notice

This sample currently doesn't run in Python 3 due to an issue with gevent. Gevent is planning to address the issue in the next release.
