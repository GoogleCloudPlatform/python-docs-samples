Cloud Media Translation Python Samples
======================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=media-translation/cloud-client/README.rst)

This directory contains samples for Cloud Media Translation. With [Cloud
Media Translation]{.title-ref}, you can dynamically translate text
between thousands of language pairs.

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

### Translate from file

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=media-translation/cloud-client/translate_from_file.py,media-translation/cloud-client/README.rst)

To run this sample:

``` {.bash}
$ python translate_from_file.py
```

### Translate from mic

To run this sample:

``` {.bash}
$ python translate_from_mic.py
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
