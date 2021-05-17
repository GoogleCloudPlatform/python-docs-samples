# google-cloud-compute library samples

These samples demonstrate usage of the google-cloud-compute library to interact
with the Google Compute Engine API.

## Running the quickstart script

### Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and 
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

1. Create a service account with the 'Editor' permissions by following these 
[instructions](https://cloud.google.com/iam/docs/creating-managing-service-accounts).

1. [Download a JSON key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) to use to authenticate your script.

1. Configure your local environment to use the acquired key.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/key.json
```

### Install requirements

Create a new virtual environment and install the required libraries.
```bash
virtualenv --python python3 name-of-your-virtualenv
source name-of-your-virtualenv/bin/activate
pip install -r requirements.txt
```

### Run the demo

Run the quickstart script, providing it with your project name, a GCP zone and a name for the instance that will be created and destroyed:
```bash
# For example, to create machine "test-instance" in europe-central2-a in project "my-test-project":
python quickstart.py my-test-project europe-central2-a test-instance
```
