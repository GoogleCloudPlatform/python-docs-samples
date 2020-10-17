Google Cloud Datastore Python Samples
=====================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=datastore/cloud-client/README.rst)

This directory contains samples for Google Cloud Datastore. [Google
Cloud Datastore](https://cloud.google.com/datastore/docs) is a NoSQL
document database built for automatic scaling, high performance, and
ease of application development.

Set environment variables:

:   [GOOGLE_CLOUD_PROJECT]{.title-ref} - Google Cloud project id
    [CLOUD_STORAGE_BUCKET]{.title-ref} - Google Cloud Storage bucket
    name

Roles to be set in your Service Account and App Engine default service account:

:   [Datastore Import Export Admin]{.title-ref}, or [Cloud Datastore
    Owner]{.title-ref}, or [Owner]{.title-ref} [Storage
    Admin]{.title-ref}, or [Owner]{.title-ref}

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

### Quickstart

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=datastore/cloud-client/quickstart.py,datastore/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python quickstart.py
```

### Tasks example app

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=datastore/cloud-client/tasks.py,datastore/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python tasks.py
```

### Snippets

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=datastore/cloud-client/snippets.py,datastore/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python snippets.py

usage: snippets.py [-h] project_id

Demonstrates datastore API operations.

positional arguments:
  project_id  Your cloud project ID.

optional arguments:
  -h, --help  show this help message and exit
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
