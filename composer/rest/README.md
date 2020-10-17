Google Cloud Composer Python Samples
====================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=composer/rest/README.rst)

This directory contains samples for Google Cloud Composer. [Google Cloud
Composer](https://cloud.google.com/composer/docs) is a managed Apache
Airflow service that helps you create, schedule, monitor and manage
workflows. Cloud Composer automation helps you create Airflow
environments quickly and use Airflow-native tools, such as the powerful
Airflow web interface and command line tools, so you can focus on your
workflows and not your infrastructure.

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

### Determine Cloud Storage path for DAGs

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=composer/rest/get_dag_prefix.py,composer/rest/README.rst)

To run this sample:

``` {.bash}
$ python get_dag_prefix.py

usage: get_dag_prefix.py [-h] project_id location composer_environment

Get a Cloud Composer environment via the REST API.

This code sample gets a Cloud Composer environment resource and prints the
Cloud Storage path used to store Apache Airflow DAGs.

positional arguments:
  project_id            Your Project ID.
  location              Region of the Cloud Composer environent.
  composer_environment  Name of the Cloud Composer environent.

optional arguments:
  -h, --help            show this help message and exit
```
