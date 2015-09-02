## Google Cloud Platform Python Samples

This repository holds the samples used in the python documentation on [cloud.google.com](https://cloud.google.com).

[![Build Status](https://travis-ci.org/GoogleCloudPlatform/python-docs-samples.svg)](https://travis-ci.org/GoogleCloudPlatform/python-docs-samples)
[![Coverage Status](https://coveralls.io/repos/GoogleCloudPlatform/python-docs-samples/badge.svg)](https://coveralls.io/r/GoogleCloudPlatform/python-docs-samples)

For more detailed introduction to a product, check the README in the corresponding folder. 

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)

## Testing

The tests in this repository run against live services, therefore, it takes a bit
of configuration to run all of the tests locally.

### Local setup

Before you can run tests locally you must have:

* The latest [tox](https://tox.readthedocs.org/en/latest/) and [pip](https://pypi.python.org/pypi/pip) installed.

        $ sudo pip install --upgrade tox pip

* The [Google Cloud SDK](https://cloud.google.com/sdk/) installed. You can do so with the following command:

        $ curl https://sdk.cloud.google.com | bash

* Most tests require you to have an active, billing-enabled project on the [Google Developers Console](https://console.developers.google.com).

* You will need a set of [Service Account Credentials](https://console.developers.google.com/project/_/apiui/credential) for your project in ``json`` form.

* Set the environment variables appropriately for your project.

        $ export GOOGLE_APPLICATION_CREDENTIALS=your-service-account-json-file
        $ export TEST_PROJECT_ID=your-project-id
        $ export TEST_BUCKET_NAME=your-bucket-name

If you want to run the Google App Engine tests, you will need:

* The App Engine Python SDK. You can install this with the Google Cloud SDK:

        $ gcloud components update gae-python

* You will need to set an additional environment variable:

        $ export GAE_PYTHONPATH=~/google-cloud-sdk/platform/google_appengine

To run the bigquery tests, you'll need to create a bigquery dataset:

* Create a dataset in your project named `test_dataset`.
* Create a table named `test_table2`, upload ``tests/resources/data.csv`` and give it the following schema:

        Name STRING
        Age INTEGER
        Weight FLOAT
        IsMagic BOOLEAN


### Test environments

We use [tox](https://tox.readthedocs.org/en/latest/) to configure multiple python environments:

* ``py27`` contains tests for samples that run in a normal Python 2.7 environment. This is (mostly) everything outside of the ``appengine`` directory.
* ``gae`` contains tests for samples that run only in Google App Engine. This is (mostly) everything in the ``appengine`` directory.
* ``pep8`` just runs the linter.

To run tests for a particular environment, invoke tox with the ``-e`` flag:

    tox -e py27

To run one particular test suite or provide additional parameters to ``nose``, invoke tox like this:

    toxe -e py27 -- storage/tests/test_list_objects.py

*Note*: The ``gae`` environment can't be told to run one particular test at this time.

## Adding new tests

There are a handful of common testing utilities are located under ``tests``, see existing tests for example usage.

When adding a new top-level directory, be sure to edit ``.coveragerc`` to include it in coveralls.

To add new tests that require Google App Engine, please place them in the ``appengine`` directory if possible. If you place them elsewhere, you will need to modify ``tox.ini`` to make the environments appropriately run or ignore your test.

## Licensing

* See [LICENSE](LICENSE)
