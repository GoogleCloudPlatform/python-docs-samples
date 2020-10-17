Google Cloud Talent Solution API Python Samples
===============================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/README.rst)

This directory contains samples for Google Cloud Talent Solution API. [Cloud Talent Solution]{.title-ref} is a service that brings machine learning to your job

:   search experience, returning high quality results to job seekers far
    beyond the limitations of typical keyword-based methods. Once
    integrated with your job content, Cloud Talent Solution
    automatically detects and infers various kinds of data, such as
    related titles, seniority, and industry.

To run the sample, you need to enable the API at:
<https://console.cloud.google.com/apis/library/jobs.googleapis.com>

To run the sample, you need to have [Talent Solution Job
Editor]{.title-ref} role.

Visit \[Data logging
page\](<https://console.cloud.google.com/talent-solution/data-permission-onboard>)
and enable the Data logging on your cloud project and connect at least
one service account.

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

### AutoCompleteSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/auto_complete_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python auto_complete_sample.py
```

### BaseCompanySample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/base_company_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python base_company_sample.py
```

### BaseJobSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/base_job_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python base_job_sample.py
```

### BatchOperationSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/batch_operation_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python batch_operation_sample.py
```

### CommuteSearchSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/commute_search_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python commute_search_sample.py
```

### CustomAttributeSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/custom_attribute_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python custom_attribute_sample.py
```

### EmailAlertSearchSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/email_alert_search_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python email_alert_search_sample.py
```

### FeaturedJobSearchSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/featured_job_search_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python featured_job_search_sample.py
```

### GeneraSearchSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/general_search_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python general_search_sample.py
```

### HistogramSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/histogram_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python histogram_sample.py
```

### LocationSearchSample

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=jobs/v2/api_client/location_search_sample.py,jobs/v2/api_client/README.rst)

To run this sample:

``` {.bash}
$ python location_search_sample.py
```
