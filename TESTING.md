# Testing

The tests in this repository are system tests and run against live services, therefore, it takes a bit of configuration to run all of the tests locally.

Before you can run tests locally you must have:

* The latest [tox](https://tox.readthedocs.org/en/latest/),
  [pip](https://pypi.python.org/pypi/pip), and [gcp-python-repo-tools](https://pypi.python.org/pypi/gcp-python-repo-tools) installed.

        $ sudo pip install --upgrade tox pip gcp-python-repo-tools

* The [Google Cloud SDK](https://cloud.google.com/sdk/) installed. You
  can do so with the following command:

        $ curl https://sdk.cloud.google.com | bash

## Preparing a project for testing

Most tests require you to have an active, billing-enabled project on the
[Google Cloud Console](https://console.cloud.google.com).

### Creating resources

Some resources need to be created in a project ahead of time before testing. We have a script that can create everything needed:

    gcloud config set project <your-project-id>
    scripts/prepare-testing-project.sh

The script will also instruct you to follow a URL to enable APIs. You will need to do that.

### Getting a service account key

From the Cloud Console, create a new Service Account and download its json key. Place this file in `testing/resources/service-account.json`.

## Environment variables

* Copy `testing/resources/test-env.tmpl.sh` to `testing/resources/test-env.sh`, and updated it with your configuration.
* Run `source testing/resources/test-env.sh`.
* Run `export GOOGLE_APPLICATION_CREDENTIALS=testing/resources/service-account.json`.

If you want to run the Google App Engine tests, you will need:

* The App Engine Python SDK. You can also download it programatically with `gcp-python-repo-tools`:

        $ gcp-python-repo-tools download-appengine-sdk <dest>

* Set the `GAE_PYTHONPATH` variable:

        $ export GAE_PYTHONPATH=<path your AppeEngine sdk>

### Test environments

We use [tox](https://tox.readthedocs.org/en/latest/) to configure
multiple python environments:

* ``py27`` and ``py34`` contains tests for samples that run in a normal Python 2.7 pr 3.4 environment. This is everything outside of the ``appengine`` directory that isn't slow or flaky.
* ``py27-all`` and ``py34-all`` runs all tests except for App Engine tests. This can time some time and some tests are flaky.
* ``gae`` contains tests for samples that run only in Google App Engine. This is (mostly) everything in the ``appengine`` directory.
* ``pep8`` just runs the linter.

To run tests for a particular environment, invoke tox with the ``-e``
flag:

    tox -e py27

To run one particular test suite or provide additional parameters to
``py.test``, invoke tox like this:

    toxe -e py27 -- storage/api

### Adding new tests

When adding a new top-level directory, be sure to edit ``.coveragerc`` and ``tox.ini`` to include it in tests and coverage reporting.

To add new tests that require Google App Engine, please place them in
the ``appengine`` directory if possible. If you place them elsewhere,
you will need to modify ``tox.ini`` to make the environments
appropriately run or ignore your test.
