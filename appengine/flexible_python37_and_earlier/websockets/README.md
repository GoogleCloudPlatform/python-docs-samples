# Python websockets sample for Google App Engine Flexible Environment

This sample demonstrates how to use websockets on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
