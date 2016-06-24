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

## Understanding the code

The [application](main.py) uses the [Google Cloud Bigtable HappyBase
package][Bigtable HappyBase], an implementation of the [HappyBase][HappyBase]
library, to make calls to Cloud Bigtable. It demonstrates several basic
concepts of working with Cloud Bigtable via this API:

[Bigtable HappyBase]: https://googlecloudplatform.github.io/gcloud-python/stable/happybase-package.html
[HappyBase]: http://happybase.readthedocs.io/en/latest/index.html

- Creating a [Connection][HappyBase Connection] to a Cloud Bigtable
  [Cluster][Cluster API].
- Using the [Connection][HappyBase Connection] interface to create, disable and
  delete a [Table][HappyBase Table].
- Using the Connection to get a Table.
- Using the Table to write rows via a [put][HappyBase Table Put] and scan
  across multiple rows using [scan][HappyBase Table Scan].

[Cluster API]: https://googlecloudplatform.github.io/gcloud-python/stable/bigtable-cluster.html
[HappyBase Connection]: https://googlecloudplatform.github.io/gcloud-python/stable/happybase-connection.html
[HappyBase Table]: https://googlecloudplatform.github.io/gcloud-python/stable/happybase-table.html
[HappyBase Table Put]: https://googlecloudplatform.github.io/gcloud-python/stable/happybase-table.html#gcloud.bigtable.happybase.table.Table.put
[HappyBase Table Scan]: https://googlecloudplatform.github.io/gcloud-python/stable/happybase-table.html#gcloud.bigtable.happybase.table.Table.scan

