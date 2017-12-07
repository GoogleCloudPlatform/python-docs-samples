# Python Google Cloud Datastore sample for Google App Engine Flexible Environment

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible/datastore/README.md

This sample demonstrates how to use [Google Cloud Datastore](https://cloud.google.com/datastore/) on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Setup

Before you can run or deploy the sample, you will need to enable the Cloud Datastore API in the [Google Developers Console](https://console.developers.google.com/project/_/apiui/apiview/datastore/overview).

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

Starting your application:

    $ python main.py
