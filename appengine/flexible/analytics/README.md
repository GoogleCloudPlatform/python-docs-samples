# Google Analytics Measurement Protocol sample for Google App Engine Flexible

This sample demonstrates how to use the [Google Analytics Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/v1/) (or any other SQL server) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Create a Google Analytics Property and obtain the Tracking ID.

2. Update the environment variables in  in ``app.yaml`` with your Tracking ID.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You will need to set the following environment variables via your shell before running the sample:

    $ export GA_TRACKING_ID=[your Tracking ID]
    $ python main.py
