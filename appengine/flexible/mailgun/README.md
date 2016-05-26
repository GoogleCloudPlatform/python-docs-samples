# Python Mailgun email sample for Google App Engine Flexible Environment

This sample demonstrates how to use [Mailgun](https://www.mailgun.com) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

For more information about Mail, see their [documentation](https://documentation.mailgun.com/).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. [Create a Mailgun Account](http://www.mailgun.com/google). As of September 2015, Google users start with 30,000 free emails per month.

2. Configure your Mailgun settings in the environment variables section in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You can run the application locally and send emails from your local machine. You
will need to set environment variables before starting your application:

    $ export MAILGUN_API_KEY=[your-mailgun-api-key]
    $ export MAILGUN_DOMAIN_NAME=[your-mailgun-domain-name]
    $ python main.py
