Cloud Healthcare API Python Samples
===================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=healthcare/api-client/fhir/README.rst)

This directory contains samples for Cloud Healthcare API. [Cloud
Healthcare API](https://cloud.google.com/healthcare/docs) implements
healthcare-native protocols and formats to accelerate ingestion,
storage, analysis, and integration of healthcare data with cloud-based
applications. - See the [migration
guide](https://cloud.google.com/vision/docs/python-client-migration) for
information about migrating to Python client library v0.25.1.

To run the sample, you need to enable the API at:
<https://console.cloud.google.com/apis/library/healthcare.googleapis.com>

To run the sample, you need to have the following roles: \* [Healthcare
Dataset Administrator]{.title-ref} \* [Healthcare FHIR Store
Administrator]{.title-ref} \* [Healthcare FHIR Resource
Editor]{.title-ref}

Setup
-----

### Authentication

This sample requires you to have authentication setup. Refer to the
[Authentication Getting Started
Guide](https://cloud.google.com/docs/authentication/getting-started) for
instructions on setting up credentials for applications.

### Install Dependencies

1.  Clone python-docs-samples and change directory to the sample
    directory you want to use.

    > ``` {.bash}
    > $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    > ```

2.  Install [pip](https://pip.pypa.io/) and
    [virtualenv](https://virtualenv.pypa.io/) if you do not already have
    them. You may want to refer to the [Python Development Environment
    Setup Guide]() for Google Cloud Platform for instructions.

    ::: {#Python Development Environment Setup Guide}
    > <https://cloud.google.com/python/setup>
    :::

3.  Create a virtualenv. Samples are compatible with Python 2.7 and
    3.4+.

    > ``` {.bash}
    > $ virtualenv env
    > $ source env/bin/activate
    > ```

4.  Install the dependencies needed to run the samples.

    > ``` {.bash}
    > $ pip install -r requirements.txt
    > ```

Samples
-------

### FHIR stores

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=healthcare/api-client/fhir/fhir_stores.py,healthcare/api-client/fhir/README.rst)

To run this sample:

``` {.bash}
$ python fhir_stores.py

usage: fhir_stores.py [-h] [--service_account_json SERVICE_ACCOUNT_JSON]
                      [--project_id PROJECT_ID] [--cloud_region CLOUD_REGION]
                      [--dataset_id DATASET_ID]
                      [--fhir_store_id FHIR_STORE_ID]
                      {create-dataset,delete-dataset,create-fhir-store,delete-fhir-store}
                      ...

positional arguments:
  {create-dataset,delete-dataset,create-fhir-store,delete-fhir-store}
    create-dataset      Creates a dataset.
    delete-dataset      Deletes a dataset.
    create-fhir-store   Creates a new FHIR store within the parent dataset.
    delete-fhir-store   Deletes the specified FHIR store.

optional arguments:
  -h, --help            show this help message and exit
  --service_account_json SERVICE_ACCOUNT_JSON
                        Path to service account JSON file.
  --project_id PROJECT_ID
                        GCP cloud project name
  --cloud_region CLOUD_REGION
                        GCP cloud region
  --dataset_id DATASET_ID
                        Name of dataset
  --fhir_store_id FHIR_STORE_ID
                        Name of FHIR store
```

### FHIR resources

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=healthcare/api-client/fhir/fhir_resources.py,healthcare/api-client/fhir/README.rst)

To run this sample:

``` {.bash}
$ python fhir_resources.py

usage: fhir_resources.py [-h] [--service_account_json SERVICE_ACCOUNT_JSON]
                         [--base_url BASE_URL] [--project_id PROJECT_ID]
                         [--cloud_region CLOUD_REGION]
                         [--dataset_id DATASET_ID]
                         [--fhir_store_id FHIR_STORE_ID]
                         [--resource_type RESOURCE_TYPE]
                         [--resource_id RESOURCE_ID] [--patient_id PATIENT_ID]
                         [--encounter_id ENCOUNTER_ID]
                         {create-patient,create-encounter,create-observation,delete-resource,conditional-delete-resource,conditional-update-resource,conditional-patch-resource}
                         ...

positional arguments:
  {create-patient,create-encounter,create-observation,delete-resource,conditional-delete-resource,conditional-update-resource,conditional-patch-resource}
    create-patient      Creates a new Patient resource in a FHIR store.
    create-encounter    Creates a new Encounter resource in a FHIR store based
                        on a Patient.
    create-observation  Creates a new Observation resource in a FHIR store
                        based on an Encounter.
    delete-resource     Deletes a FHIR resource. Regardless of whether the
                        operation succeeds or fails, the server returns a 200
                        OK HTTP status code. To check that the resource was
                        successfully deleted, search for or get the resource
                        and see if it exists.
    conditional-delete-resource
                        Deletes FHIR resources that match a search query.
    conditional-update-resource
                        If a resource is found based on the search criteria
                        specified in the query parameters, updates the entire
                        contents of that resource.
    conditional-patch-resource
                        If a resource is found based on the search criteria
                        specified in the query parameters, updates part of
                        that resource by applying the operations specified in
                        a JSON Patch document.

optional arguments:
  -h, --help            show this help message and exit
  --service_account_json SERVICE_ACCOUNT_JSON
                        Path to service account JSON file.
  --base_url BASE_URL   Healthcare API URL.
  --project_id PROJECT_ID
                        GCP project name
  --cloud_region CLOUD_REGION
                        GCP region
  --dataset_id DATASET_ID
                        Name of dataset
  --fhir_store_id FHIR_STORE_ID
                        Name of FHIR store
  --resource_type RESOURCE_TYPE
                        The type of resource. First letter must be capitalized
  --resource_id RESOURCE_ID
                        Identifier for a FHIR resource
  --patient_id PATIENT_ID
                        Identifier for a Patient resource. Can be used as a
                        reference for an Encounter/Observation
  --encounter_id ENCOUNTER_ID
                        Identifier for an Encounter resource. Can be used as a
                        reference for an Observation
```

The client library
------------------

This sample uses the [Google Cloud Client Library for
Python](https://googlecloudplatform.github.io/google-cloud-python/). You
can read the documentation for more details on API usage and use GitHub
to [browse the
source](https://github.com/GoogleCloudPlatform/google-cloud-python) and
[report
issues](https://github.com/GoogleCloudPlatform/google-cloud-python/issues).
