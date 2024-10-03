# Anti Money Laundering AI Python Samples

This directory contains samples for Anti Money Laundering AI (AML AI). Use this API to produce risk scores and accompanying explainability output to support your alerting and investigation process. For more information, see the
[Anti Money Laundering AI documentation](https://cloud.google.com/financial-services/anti-money-laundering/).

## Setup

To run the samples, you need to first follow the steps in
[Set up a project and permissions](https://cloud.google.com/financial-services/anti-money-laundering/docs/set-up-project-permissions).

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

Make sure to enable the AML AI API on the test project. Set the following
environment variable:

*   `GOOGLE_CLOUD_PROJECT`
