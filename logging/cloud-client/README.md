Stackdriver Logging Python Samples
==================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=logging/cloud-client/README.rst)

This directory contains samples for [Cloud
Logging](https://cloud.google.com/logging/docs), which you can use to
store, search, analyze, monitor, and alert on log data and events from
Google Cloud Platform and Amazon Web Services.

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

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=logging/cloud-client/quickstart.py,logging/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python quickstart.py
```

### Snippets

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=logging/cloud-client/snippets.py,logging/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python snippets.py

usage: snippets.py [-h] logger_name {list,write,delete} ...

This application demonstrates how to perform basic operations on logs and
log entries with Stackdriver Logging.

For more information, see the README.md under /logging and the
documentation at https://cloud.google.com/logging/docs.

positional arguments:
  logger_name          Logger name
  {list,write,delete}
    list               Lists the most recent entries for a given logger.
    write              Writes log entries to the given logger.
    delete             Deletes a logger and all its entries. Note that a
                       deletion can take several minutes to take effect.

optional arguments:
  -h, --help           show this help message and exit
```

### Export

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=logging/cloud-client/export.py,logging/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python export.py

usage: export.py [-h] {list,create,update,delete} ...

positional arguments:
  {list,create,update,delete}
    list                Lists all sinks.
    create              Lists all sinks.
    update              Changes a sink's filter. The filter determines which
                        logs this sink matches and will be exported to the
                        destination. For example a filter of 'severity>=INFO'
                        will send all logs that have a severity of INFO or
                        greater to the destination. See https://cloud.google.c
                        om/logging/docs/view/advanced_filters for more filter
                        information.
    delete              Deletes a sink.

optional arguments:
  -h, --help            show this help message and exit
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
