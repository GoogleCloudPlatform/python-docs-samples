# Cloud Bigtable Hello World

This is a simple application that demonstrates using the [Google Cloud Client
Library][gcloud-python] to connect to and interact with Cloud Bigtable.

[gcloud-python]: https://github.com/GoogleCloudPlatform/gcloud-python


## Provision a cluster

Follow the instructions in the [user documentation](https://cloud.google.com/bigtable/docs/creating-cluster)
to create a Google Cloud Platform project and Cloud Bigtable cluster if necessary.
You'll need to reference your project ID, zone and cluster ID to run the application.


## Run the application

First, set your [Google Application Default Credentials](https://developers.google.com/identity/protocols/application-default-credentials)

Install the dependencies with pip.

```
$ pip install -r requirements.txt
```

Run the application. Replace the command-line parameters with values for your cluster.

```
$ python main.py my-project my-cluster us-central1-c
```

You will see output resembling the following:

```
Create table Hello-Bigtable-1234
Write some greetings to the table
Scan for all greetings:
        greeting0: Hello World!
        greeting1: Hello Cloud Bigtable!
        greeting2: Hello HappyBase!
Delete table Hello-Bigtable-1234
```
