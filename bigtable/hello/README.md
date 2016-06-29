# Cloud Bigtable Hello World

This is a simple application that demonstrates using the [Google Cloud Client
Library][gcloud-python-bigtable] to connect to and interact with Cloud Bigtable.

<!-- auto-doc-link -->
These samples are used on the following documentation page:

> https://cloud.google.com/bigtable/docs/samples-python-hello

<!-- end-auto-doc-link -->

[gcloud-python-bigtable]: https://googlecloudplatform.github.io/gcloud-python/stable/bigtable-usage.html
[sample-docs]: https://cloud.google.com/bigtable/docs/samples-python-hello


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Downloading the sample](#downloading-the-sample)
- [Costs](#costs)
- [Provisioning an instance](#provisioning-an-instance)
- [Running the application](#running-the-application)
- [Cleaning up](#cleaning-up)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Downloading the sample

Download the sample app and navigate into the app directory:

1.  Clone the [Python samples
    repository](https://github.com/GoogleCloudPlatform/python-docs-samples), to
    your local machine:

        git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

    Alternatively, you can [download the
    sample](https://github.com/GoogleCloudPlatform/python-docs-samples/archive/master.zip)
    as a zip file and extract it.

2.  Change to the sample directory.

        cd python-docs-samples/bigtable/hello


## Costs

This sample uses billable components of Cloud Platform, including:

+   Google Cloud Bigtable

Use the [Pricing Calculator][bigtable-pricing] to generate a cost estimate
based on your projected usage.  New Cloud Platform users might be eligible for
a [free trial][free-trial].

[bigtable-pricing]: https://cloud.google.com/products/calculator/#id=1eb47664-13a2-4be1-9d16-6722902a7572
[free-trial]: https://cloud.google.com/free-trial


## Provisioning an instance

Follow the instructions in the [user
documentation](https://cloud.google.com/bigtable/docs/creating-instance) to
create a Google Cloud Platform project and Cloud Bigtable instance if necessary.
You'll need to reference your project id and instance id to run the
application.


## Running the application

First, set your [Google Application Default Credentials](https://developers.google.com/identity/protocols/application-default-credentials)

Install the dependencies with pip.

```
$ pip install -r requirements.txt
```

Run the application. Replace the command-line parameters with values for your instance.

```
$ python main.py my-project my-instance
```

You will see output resembling the following:

```
Create table Hello-Bigtable
Write some greetings to the table
Scan for all greetings:
        greeting0: Hello World!
        greeting1: Hello Cloud Bigtable!
        greeting2: Hello HappyBase!
Delete table Hello-Bigtable
```


## Cleaning up

To avoid incurring extra charges to your Google Cloud Platform account, remove
the resources created for this sample.

- [Delete the Cloud Bigtable
  instance](https://cloud.google.com/bigtable/docs/deleting-instance).
