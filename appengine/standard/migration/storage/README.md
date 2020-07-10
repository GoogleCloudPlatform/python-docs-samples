## App Engine cloudstorage library Replacement

The runtime for App Engine standard for Python 2.7 includes the `cloudstorage`
library, which is used to store and retrieve blobs. The sample in this
directory shows how to do the same operations using Python libraries that
work in either App Engine standard for Python runtime, version 2.7 or 3.7.
The sample code is the same for each environment.

To deploy and run this sample in App Engine standard for Python 2.7:

    pip install -t lib -r requirements.txt
    gcloud app deploy

To deploy and run this sample in App Engine standard for Python 3.7:

    gcloud app deploy app3.yaml
