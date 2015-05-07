appengine-ndb-snippets
======================

Sample code snippets for NDB.

How to run the test
===================

To run the tests, please install App Engine Python SDK and tox and run
tox with the environment variable PYTHONPATH to the App Engine Python SDK.

You can install App Engine Python SDK with [Google Cloud SDK](https://cloud.google.com/sdk/) with the following command:

    $ gcloud components update gae-python

Here is instructions to run the tests with virtualenv, $GCLOUD is your
Google Cloud SDK installation path.

    $ virtualenv -p python2.7 --no-site-packages .
    $ source bin/activate
    $ pip install tox
    $ env PYTHONPATH=${GCLOUD}/platform/google_appengine tox
