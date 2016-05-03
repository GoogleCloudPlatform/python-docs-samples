# Python Mailjet email sample for Google App Engine Flexible

This sample demonstrates how to use [Mailjet](https://www.mailgun.com) on [Google App Engine Flexible](https://cloud.google.com/appengine/docs/flexible/).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. [Create a Mailjet Account](http://www.mailjet.com/google).

2. Configure your Mailjet settings in the environment variables section in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You can run the application locally and send emails from your local machine. You
will need to set environment variables before starting your application:

    $ export MAILGUN_API_KEY=[your-mailgun-api-key]
    $ export MAILGUN_API_SECRET=[your-mailgun-secret]
    $ export MAILGUN_SENDER=[your-sender-address]
    $ python main.py
