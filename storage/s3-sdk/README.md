Google Cloud Storage Python Samples
===================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/README.rst)

This directory contains samples for Google Cloud Storage. [Google Cloud
Storage](https://cloud.google.com/storage/docs) provides support for S3
API users through the GCS XML API. Learn more about migrating data from
S3 to GCS at <https://cloud.google.com/storage/docs/migrating>.

Setup
-----

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

### List GCS Buckets using S3 SDK

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/list_gcs_buckets.py,storage/s3-sdk/README.rst)

To run this sample:

``` {.bash}
$ python list_gcs_buckets.py

usage: list_gcs_buckets.py [-h] google_access_key_id google_access_key_secret

positional arguments:
  google_access_key_id  Your Cloud Storage HMAC Access Key ID.
  google_access_key_secret
                        Your Cloud Storage HMAC Access Key Secret.

optional arguments:
  -h, --help            show this help message and exit
```

### List GCS Objects using S3 SDK

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/s3-sdk/list_gcs_objects.py,storage/s3-sdk/README.rst)

To run this sample:

``` {.bash}
$ python list_gcs_objects.py

usage: list_gcs_objects.py [-h]
                           google_access_key_id google_access_key_secret
                           bucket_name

positional arguments:
  google_access_key_id  Your Cloud Storage HMAC Access Key ID.
  google_access_key_secret
                        Your Cloud Storage HMAC Access Key Secret.
  bucket_name           Your Cloud Storage bucket name

optional arguments:
  -h, --help            show this help message and exit
```
