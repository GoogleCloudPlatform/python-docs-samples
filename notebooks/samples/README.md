# AI Platform Notebooks API code samples

Sample command-line programs for interacting with the Notebooks API.

## Prerequisites to run locally:

* [Python 3](https://www.python.org/downloads/)
* [pip](https://pypi.python.org/pypi/pip)

Go to the [Google Cloud Console](https://console.cloud.google.com).

Under API Manager, search for the Google Cloud Notebooks API and enable
it. You can also enable API via Command Line: 

```bash
gcloud services enable notebooks.googleapis.com
```

## Set Up Your Local Dev Environment

To install, run the following commands. If you want to use
[virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv. 

```bash
pip install -r requirements.txt
```

**Note:** While this sample demonstrates interacting with Notebooks via
the API, the functionality demonstrated here could also be accomplished
using the Cloud Console or the
[gcloud CLI](https://cloud.google.com/sdk/gcloud/reference/beta/notebooks)

## Authentication

Please see the
[Google cloud authentication guide](https://cloud.google.com/docs/authentication/).
The recommended approach to running these samples is a Service Account
with a JSON key.
