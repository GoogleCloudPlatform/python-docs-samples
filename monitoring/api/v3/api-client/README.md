Stackdriver Monitoring Python Samples
=====================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=monitoring/api/v3/api-client/README.rst)

This directory contains samples for Stackdriver Monitoring. [Stackdriver
Monitoring ](https://cloud.google.com/monitoring/docs) collects metrics,
events, and metadata from Google Cloud Platform, Amazon Web Services
(AWS), hosted uptime probes, application instrumentation, and a variety
of common application components including Cassandra, Nginx, Apache Web
Server, Elasticsearch and many others. Stackdriver ingests that data and
generates insights via dashboards, charts, and alerts.

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

### List resources

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=monitoring/api/v3/api-client/list_resources.py,monitoring/api/v3/api-client/README.rst)

To run this sample:

``` {.bash}
$ python list_resources.py

usage: list_resources.py [-h] --project_id PROJECT_ID

 Sample command-line program for retrieving Stackdriver Monitoring API V3
data.

See README.md for instructions on setting up your development environment.

To run locally:

    python list_resources.py --project_id=<YOUR-PROJECT-ID>

optional arguments:
  -h, --help            show this help message and exit
  --project_id PROJECT_ID
                        Project ID you want to access.
```

### Custom metrics

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=monitoring/api/v3/api-client/custom_metric.py,monitoring/api/v3/api-client/README.rst)

To run this sample:

``` {.bash}
$ python custom_metric.py

usage: custom_metric.py [-h] --project_id PROJECT_ID

 Sample command-line program for writing and reading Stackdriver Monitoring
API V3 custom metrics.

Simple command-line program to demonstrate connecting to the Google
Monitoring API to write custom metrics and read them back.

See README.md for instructions on setting up your development environment.

This example creates a custom metric based on a hypothetical GAUGE measurement.

To run locally:

    python custom_metric.py --project_id=<YOUR-PROJECT-ID>

optional arguments:
  -h, --help            show this help message and exit
  --project_id PROJECT_ID
                        Project ID you want to access.
```
