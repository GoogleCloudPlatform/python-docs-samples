# How to become a contributor and submit your own code

## Contributor License Agreements

We'd love to accept your sample apps and patches! Before we can take them, we
have to jump a couple of legal hurdles.

Please fill out either the individual or corporate Contributor License
Agreement (CLA).

  * If you are an individual writing original source code and you're sure you
    own the intellectual property, then you'll need to sign an [individual CLA]
    (https://developers.google.com/open-source/cla/individual).
  * If you work for a company that wants to allow you to contribute your work,
    then you'll need to sign a [corporate CLA]
    (https://developers.google.com/open-source/cla/corporate).

Follow either of the two links above to access the appropriate CLA and
instructions for how to sign and return it. Once we receive it, we'll
be able to accept your pull requests.

## Contributing A Patch

1. Submit an issue describing your proposed change to the repo in question.
1. The repo owner will respond to your issue promptly.
1. If your proposed change is accepted, and you haven't already done so, sign a
   Contributor License Agreement (see details above).
1. Fork the desired repo, develop and test your code changes.
1. Ensure that your code adheres to the existing style in the sample to which
   you are contributing. Refer to the
   [Google Cloud Platform Samples Style Guide]
   (https://github.com/GoogleCloudPlatform/Template/wiki/style.html) for the
   recommended coding standards for this organization.
1. Ensure that your code has an appropriate set of unit tests which all pass.
1. Submit a pull request.

## Testing

The tests in this repository run against live services, therefore, it
takes a bit of configuration to run all of the tests locally.

### Local setup

Before you can run tests locally you must have:

* The latest [tox](https://tox.readthedocs.org/en/latest/) and
  [pip](https://pypi.python.org/pypi/pip) installed.

        $ sudo pip install --upgrade tox pip

* The [Google Cloud SDK](https://cloud.google.com/sdk/) installed. You
  can do so with the following command:

        $ curl https://sdk.cloud.google.com | bash

* Most tests require you to have an active, billing-enabled project on
  the
  [Google Developers Console](https://console.developers.google.com).

* You will need a set of
  [Service Account Credentials](https://console.developers.google.com/project/_/apiui/credential)
  for your project in ``json`` form.

* Set the environment variables appropriately for your project.

        $ export GOOGLE_APPLICATION_CREDENTIALS=your-service-account-json-file
        $ export TEST_PROJECT_ID=your-project-id
        $ export TEST_BUCKET_NAME=your-bucket-name

If you want to run the Google App Engine tests, you will need:

* The App Engine Python SDK. You can install this by downloading it [here]
(https://cloud.google.com/appengine/downloads?hl=en)

* You can also download it programatically with the
  tests/scripts/fetch_gae_sdk.py

        $ test/scripts/fetch_gae_sdk.py <dest dir>

* You will need to set an additional environment variable:

        $ export GAE_PYTHONPATH=<path your AppeEngine sdk>

To run the bigquery tests, you'll need to create a bigquery dataset:

* Create a dataset in your project named `test_dataset`.
* Create a table named `test_table2`, upload ``tests/resources/data.csv`` and give it the following schema:

        Name STRING
        Age INTEGER
        Weight FLOAT
        IsMagic BOOLEAN


### Test environments

We use [tox](https://tox.readthedocs.org/en/latest/) to configure
multiple python environments:

* ``py27`` contains tests for samples that run in a normal Python 2.7
  environment. This is (mostly) everything outside of the
  ``appengine`` directory.
* ``gae`` contains tests for samples that run only in Google App
  Engine. This is (mostly) everything in the ``appengine`` directory.
* ``pep8`` just runs the linter.

To run tests for a particular environment, invoke tox with the ``-e``
flag:

    tox -e py27

To run one particular test suite or provide additional parameters to
``nose``, invoke tox like this:

    toxe -e py27 -- storage/tests/test_list_objects.py

*Note*: The ``gae`` environment can't be told to run one particular
 test at this time.

## Adding new tests

There are a handful of common testing utilities are located under
``tests``, see existing tests for example usage.

When adding a new top-level directory, be sure to edit ``.coveragerc``
to include it in coveralls.

To add new tests that require Google App Engine, please place them in
the ``appengine`` directory if possible. If you place them elsewhere,
you will need to modify ``tox.ini`` to make the environments
appropriately run or ignore your test.

