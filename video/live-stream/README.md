# Live Stream API Python Samples

This directory contains samples for the Live Stream API. Use this API to
transcode live, linear video streams into a variety of formats. The Live Stream
API benefits broadcasters, production companies, businesses, and individuals
looking to transform their live video content for use across a variety of user
devices. For more information, see the
[Live Stream API documentation](https://cloud.google.com/livestream/).

## Setup

To run the samples, you need to first follow the steps in
[Before you begin](https://cloud.google.com/livestream/docs/how-to/before-you-begin).

For more information on authentication, refer to the
[Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started).

## Install Dependencies

1. Clone python-docs-samples repository and change directories to the sample directory
you want to use.

        $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

1. Install [pip](https://pip.pypa.io/) and
[virtualenv](https://virtualenv.pypa.io/) if you do not already have them. You
may want to refer to the
[Python Development Environment Setup Guide](https://cloud.google.com/python/setup)
for Google Cloud Platform for instructions.

1. Create a virtualenv. Samples are compatible with Python 3.6+.

        $ virtualenv env
        $ source env/bin/activate

1. Install the dependencies needed to run the samples.

        $ pip install -r requirements.txt

## Testing

Make sure to enable the Live Stream API on the test project. Set the following
environment variable:

*   `GOOGLE_CLOUD_PROJECT`
