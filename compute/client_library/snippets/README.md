# google-cloud-compute library samples

These samples demonstrate usage of the google-cloud-compute library to interact
with the Google Compute Engine API.

## Running the quickstart script

### Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and 
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

1. Use `gcloud auth application-default login` to allow the script to authenticate using
your credentials to the Google Cloud APIs.

### Install requirements

Create a new virtual environment and install the required libraries.
```bash
virtualenv --python python3 name-of-your-virtualenv
source name-of-your-virtualenv/bin/activate
pip install -r ../requirements.txt
```

### Run the demo

Run the quickstart script, it will create and destroy a `n1-standard-1` 
type machine in the `europe-central2-b` zone.
```bash
python quickstart.py
```
