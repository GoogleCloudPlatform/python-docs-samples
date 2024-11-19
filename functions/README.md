<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Google Cloud Run functions Python Samples

This directory contains samples for Google Cloud Run functions.

[Cloud Run functions](https://cloud.google.com/functions/docs/concepts/overview) is a lightweight, event-based, asynchronous compute solution that allows you to create small, single-purpose functions that respond to Cloud events without the need to manage a server or a runtime environment.

There are two versions of Cloud Run functions:

* **Cloud Run functions**, formerly known as Cloud Functions (2nd gen), which deploys your function as services on Cloud Run, allowing you to trigger them using Eventarc and Pub/Sub. Cloud Run functions are created using `gcloud functions` or `gcloud run`. Samples for Cloud Run functions can be found in the [`functions/v2`](v2/) folder.
* **Cloud Run functions (1st gen)**, formerly known as Cloud Functions (1st gen), the original version of functions with limited event triggers and configurability. Cloud Run functions (1st gen) are created using `gcloud functions --no-gen2`. Samples for Cloud Run functions (1st generation) can be found in the current `functions/` folder.

## Setup

### Authentication

This sample requires you to have authentication setup. Refer to the
[Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started) for instructions on setting up
credentials for applications.

### Install Dependencies

1. Install [`pip`](https://pip.pypa.io/) and [`virtualenv`](https://virtualenv.pypa.io/) if you do not already have them. You may want to refer to the [Python Development Environment Setup Guide](https://cloud.google.com/python/setup) for Google Cloud Platform for instructions.

1. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.

```shell
virtualenv env
source env/bin/activate
```

2. Install the dependencies needed to run the samples.

```shell
pip install -r requirements.txt
```

## Samples

* [Hello World](v2/helloworld/)
* [Logging & Monitoring](v2/log/)
* [Pub/Sub functions](v2/pubsub/)

## The client library

This sample uses the [Google Cloud Client Library for Python](https://googlecloudplatform.github.io/google-cloud-python/).
You can read the documentation for more details on API usage and use GitHub
to [browse the source](https://github.com/GoogleCloudPlatform/google-cloud-python) and  [report issues]( https://github.com/GoogleCloudPlatform/google-cloud-python/issues).