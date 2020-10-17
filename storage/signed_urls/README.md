Google Cloud Storage Python Samples
===================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/signed_urls/README.rst)

This directory contains samples for Google Cloud Storage. [Google Cloud
Storage](https://cloud.google.com/storage/docs) allows world-wide
storage and retrieval of any amount of data at any time.

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

### Generate Signed URLs in Python

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/signed_urls/generate_signed_urls.py,storage/signed_urls/README.rst)

To run this sample:

``` {.bash}
$ python generate_signed_urls.py

usage: generate_signed_urls.py [-h]
                               service_account_file request_method bucket_name
                               object_name expiration

positional arguments:
  service_account_file  Path to your Google service account.
  request_method        A request method, e.g GET, POST.
  bucket_name           Your Cloud Storage bucket name.
  object_name           Your Cloud Storage object name.
  expiration            Expiration Time.

optional arguments:
  -h, --help            show this help message and exit
```
