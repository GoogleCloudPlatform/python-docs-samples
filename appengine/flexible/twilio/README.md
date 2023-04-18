# Python Twilio voice and SMS sample for Google App Engine Flexible Environment

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible/twilio/README.md

This sample demonstrates how to use [Twilio](https://www.twilio.com) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

For more information about Twilio, see their [Python quickstart tutorials](https://www.twilio.com/docs/quickstart/python).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. [Create a Twilio Account](http://ahoy.twilio.com/googlecloudplatform). Google App Engine
customers receive a complimentary credit for SMS messages and inbound messages.

2. Create a number on twilio, and configure the voice request URL to be ``https://your-app-id.appspot.com/call/receive``
and the SMS request URL to be ``https://your-app-id.appspot.com/sms/receive``.

3. Configure your Twilio settings in the environment variables section in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You can run the application locally to test the callbacks and SMS sending. You
will need to set environment variables before starting your application:

    $ export TWILIO_ACCOUNT_SID=[your-twilio-account-sid]
    $ export TWILIO_AUTH_TOKEN=[your-twilio-auth-token]
    $ export TWILIO_NUMBER=[your-twilio-number]
    $ python main.py
