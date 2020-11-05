# Transcoder API Python Samples

This directory contains samples for the Transcoder API. Use this API to transcode videos into a variety of formats. The Transcoder API benefits broadcasters, production companies, businesses, and individuals looking to transform their video content for use across a variety of user devices. For more information, see the [Transcoder API documentation](https://cloud.google.com/transcoder/).

## Setup

To run the samples, you need to first follow the steps in [Before you begin](https://cloud.google.com/transcoder/docs/how-to/before-you-begin).

For more information on authentication, refer to the
[Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started).

## Install Dependencies

1. Clone python-docs-samples and change directory to the sample directory you want to use.

        $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

1. Install [pip](https://pip.pypa.io/) and [virtualenv](https://virtualenv.pypa.io/) if you do not already have them. You may want to refer to the [Python Development Environment Setup Guide](https://cloud.google.com/python/setup) for Google Cloud Platform for instructions.

1. Create a virtualenv. Samples are compatible with Python 3.6+.

        $ virtualenv env
        $ source env/bin/activate

1. Install the dependencies needed to run the samples.

        $ pip install -r requirements.txt

## The client library

This sample uses the [Google Cloud Client Library for Python](https://googlecloudplatform.github.io/google-cloud-python/).
You can read the documentation for more details on API usage and use GitHub
to [browse the source](https://github.com/GoogleCloudPlatform/google-cloud-python) and [report issues](https://github.com/GoogleCloudPlatform/google-cloud-python/issues).

## Testing

Make sure to enable the Transcoder API on the test project. Set the following environment variables:

*   `GOOGLE_CLOUD_PROJECT`
*   `GOOGLE_CLOUD_PROJECT_NUMBER`
