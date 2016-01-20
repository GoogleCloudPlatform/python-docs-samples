# Python Google Cloud SQL sample for Google App Engine Managed VMs

This sample demonstrates how to use [Google Cloud SQL](https://cloud.google.com/sql/) (or any other SQL server) on [Google App Engine Managed VMs](https://cloud.google.com/appengine).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. Create a Cloud SQL instance. You can do this from the [Google Developers Console](https://console.developers.google.com) or via the [Cloud SDK](https://cloud.google.com/sdk). To create it via the SDK use the following command:

        $ gcloud sql instances create [your-instance-name] \
            --assign-ip \
            --authorized-networks 0.0.0.0/0 \
            --tier D0

2. Create a new user and database for the application. The easiest way to do this is via the [Google Developers Console](https://console.developers.google.com/project/_/sql/instances/example-instance2/access-control/users). Alternatively, you can use MySQL tools such as the command line client or workbench, but you will need to set a root password for your database using `gcloud sql instances set-root-password`.

3. Update the connection string in ``app.yaml`` with your instance values.

4. Finally, run ``create_tables.py`` to ensure that the database is properly configured and to create the tables needed for the sample.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You will need to set the following environment variables via your shell before running the sample:

    $ export SQLALCHEMY_DATABASE_URI=[your connection string]
    $ python main.py
