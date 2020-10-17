Google Cloud Storage Python Samples
===================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/transfer_service/README.rst)

This directory contains samples for Google Cloud Storage. [Google Cloud
Storage](https://cloud.google.com/storage/docs) allows world-wide
storage and retrieval of any amount of data at any time.

These samples demonstrate how to transfer data between Google Cloud
Storage and other storage systems.

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

### Transfer to GCS Nearline

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/transfer_service/nearline_request.py,storage/transfer_service/README.rst)

To run this sample:

``` {.bash}
$ python nearline_request.py

usage: nearline_request.py [-h]
                           description project_id start_date start_time
                           source_bucket sink_bucket

Command-line sample that creates a daily transfer from a standard
GCS bucket to a Nearline GCS bucket for objects untouched for 30 days.

This sample is used on this page:

    https://cloud.google.com/storage/transfer/create-transfer

For more information, see README.md.

positional arguments:
  description    Transfer description.
  project_id     Your Google Cloud project ID.
  start_date     Date YYYY/MM/DD.
  start_time     UTC Time (24hr) HH:MM:SS.
  source_bucket  Standard GCS bucket name.
  sink_bucket    Nearline GCS bucket name.

optional arguments:
  -h, --help     show this help message and exit
```

### Transfer from AWS

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/transfer_service/aws_request.py,storage/transfer_service/README.rst)

To run this sample:

``` {.bash}
$ python aws_request.py

usage: aws_request.py [-h]
                      description project_id start_date start_time
                      source_bucket access_key_id secret_access_key
                      sink_bucket

Command-line sample that creates a one-time transfer from Amazon S3 to
Google Cloud Storage.

This sample is used on this page:

    https://cloud.google.com/storage/transfer/create-transfer

For more information, see README.md.

positional arguments:
  description        Transfer description.
  project_id         Your Google Cloud project ID.
  start_date         Date YYYY/MM/DD.
  start_time         UTC Time (24hr) HH:MM:SS.
  source_bucket      AWS source bucket name.
  access_key_id      Your AWS access key id.
  secret_access_key  Your AWS secret access key.
  sink_bucket        GCS sink bucket name.

optional arguments:
  -h, --help         show this help message and exit
```

### Check transfer status

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=storage/transfer_service/transfer_check.py,storage/transfer_service/README.rst)

To run this sample:

``` {.bash}
$ python transfer_check.py

usage: transfer_check.py [-h] project_id job_name

Command-line sample that checks the status of an in-process transfer.

This sample is used on this page:

    https://cloud.google.com/storage/transfer/create-transfer

For more information, see README.md.

positional arguments:
  project_id  Your Google Cloud project ID.
  job_name    Your job name.

optional arguments:
  -h, --help  show this help message and exit
```
