Google Cloud Service Directory Python Samples
=============================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=servicedirectory/README.rst)

This directory contains samples for Google Cloud Service Directory.
[Google Cloud Service
Directory](https://cloud.google.com/service-directory/docs/) is a
platform for discovering, publishing, and connecting services. It offers
customers a single place to register and discover their services in a
consistent and reliable way, regardless of their environment. These
sample Java applications demonstrate how to access the Service Directory
API using the Google Java API Client Libraries.

To run the sample, you need to enable the API at:
<https://console.developers.google.com/apis/api/servicedirectory.googleapis.com/overview>

To run the sample, you need to have [Service Directory
Admin]{.title-ref} role.

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

### Snippets

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=servicedirectory/snippets.py,servicedirectory/README.rst)

To run this sample:

``` {.bash}
$ python snippets.py
```
