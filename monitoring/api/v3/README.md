# Cloud Monitoring v3 Sample

Sample command-line programs for retrieving Google Monitoring API V3 data.

`list_resources.py` is a simple command-line program to demonstrate connecting to the Google
Monitoring API to retrieve API data and print out some of the resources.

`custom_metric.py` demonstrates how to create a custom metric and write a TimeSeries
value to it.

## Prerequisites to run locally:

* [pip](https://pypi.python.org/pypi/pip)

Go to the [Google Cloud Console](https://console.cloud.google.com).

* Go to API Manager -> Credentials
* Click 'New Credentials', and create a Service Account or [click  here](https://console.cloud.google
.com/project/_/apiui/credential/serviceaccount)
 Download the JSON for this service account, and set the `GOOGLE_APPLICATION_CREDENTIALS`
 environment variable to point to the file containing the JSON credentials.


    export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/<project-id>-0123456789abcdef.json


# Set Up Your Local Dev Environment
To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

    * pip install -r requirements.txt

To run locally:

    python list_resources.py --project_id=<YOUR-PROJECT-ID>
    python custom_metric.py --project_id=<YOUR-PROJECT-ID


## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)

## Licensing

* See [LICENSE](LICENSE)


