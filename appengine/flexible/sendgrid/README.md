# Python SendGrid email sample for Google App Engine Flexible

This sample demonstrates how to use [SendGrid](https://www.sendgrid.com) on [Google App Engine Flexible](https://cloud.google.com/appengine).

For more information about SendGrid, see their [documentation](https://sendgrid.com/docs/User_Guide/index.html).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. [Create a SendGrid Account](http://sendgrid.com/partner/google). As of September 2015, Google users start with 25,000 free emails per month.

2. Configure your SendGrid settings in the environment variables section in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You can run the application locally and send emails from your local machine. You
will need to set environment variables before starting your application:

    $ export SENDGRID_API_KEY=[your-sendgrid-api-key]
    $ export SENDGRID_SENDER=[your-sendgrid-sender-email-address]
    $ python main.py
