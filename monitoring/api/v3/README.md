# Cloud Monitoring v3 Sample

Sample command-line programs for retrieving Stackdriver Monitoring API V3 data.

`list_resources.py` is a simple command-line program to demonstrate connecting to the Google
Monitoring API to retrieve API data and print out some of the resources.

`custom_metric.py` demonstrates how to create a custom metric and write a TimeSeries
value to it.

## Prerequisites to run locally:

* [pip](https://pypi.python.org/pypi/pip)

Go to the [Google Cloud Console](https://console.cloud.google.com).


# Set Up Your Local Dev Environment
To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

    * pip install -r requirements.txt

Create local credentials by running the following command and following the oauth2 flow:

    gcloud beta auth application-default login

To run:

    python list_resources.py --project_id=<YOUR-PROJECT-ID>
    python custom_metric.py --project_id=<YOUR-PROJECT-ID


## Running on GCE, GAE, or other environments

On Google App Engine, the credentials should be found automatically.

On Google Compute Engine, the credentials should be found automatically, but require that
you create the instance with the correct scopes. 

    gcloud compute instances create --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/compute.readonly" test-instance

If you did not create the instance with the right scopes, you can still upload a JSON service 
account and set GOOGLE_APPLICATION_CREDENTIALS as described below.


## Using a Service Account

In non-Google Cloud environments, GCE instances created without the correct scopes, or local
workstations if the `gcloud beta auth application-default login` command fails, use a Service 
Account by doing the following:

* Go to API Manager -> Credentials
* Click 'New Credentials', and create a Service Account or [click  here](https://console.cloud.google
.com/project/_/apiui/credential/serviceaccount)
 Download the JSON for this service account, and set the `GOOGLE_APPLICATION_CREDENTIALS`
 environment variable to point to the file containing the JSON credentials.


    export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/<project-id>-0123456789abcdef.json


## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)

## Licensing

* See [LICENSE](LICENSE)


