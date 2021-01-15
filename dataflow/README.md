# Getting started with Google Cloud Dataflow

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/README.md)

[Apache Beam](https://beam.apache.org/)
is an open source, unified model for defining both batch and streaming data-parallel processing pipelines.
This guides you through all the steps needed to run an Apache Beam pipeline in the
[Google Cloud Dataflow](https://cloud.google.com/dataflow) runner.

## Setting up your Google Cloud project

The following instructions help you prepare your Google Cloud project.

1. Install the [Cloud SDK](https://cloud.google.com/sdk/docs/).
   > *Note:* This is not required in
   > [Cloud Shell](https://console.cloud.google.com/cloudshell/editor)
   > since it already has the Cloud SDK pre-installed.

1. Create a new Google Cloud project via the
   [*New Project* page](https://console.cloud.google.com/projectcreate),
   or via the `gcloud` command line tool.

   ```sh
   export PROJECT=your-google-cloud-project-id
   gcloud projects create $PROJECT
   ```

1. Setup the Cloud SDK to your GCP project.

   ```sh
   gcloud init
   ```

1. [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project).

1. [Enable the Dataflow API](https://console.cloud.google.com/flows/enableapi?apiid=dataflow).

1. Create a service account JSON key via the
   [*Create service account key* page](https://console.cloud.google.com/apis/credentials/serviceaccountkey),
   or via the `gcloud` command line tool.
   Here is how to do it through the *Create service account key* page.

   * From the **Service account** list, select **New service account**.
   * In the **Service account name** field, enter a name.
   * From the **Role** list, select **Project > Owner** **(*)**.
   * Click **Create**. A JSON file that contains your key downloads to your computer.

   Alternatively, you can use `gcloud` through the command line.

   ```sh
   export PROJECT=$(gcloud config get-value project)
   export SA_NAME=samples
   export IAM_ACCOUNT=$SA_NAME@$PROJECT.iam.gserviceaccount.com

   # Create the service account.
   gcloud iam service-accounts create $SA_NAME --display-name $SA_NAME

   # Set the role to Project Owner (*).
   gcloud projects add-iam-policy-binding $PROJECT \
     --member serviceAccount:$IAM_ACCOUNT \
     --role roles/owner

   # Create a JSON file with the service account credentials.
   gcloud iam service-accounts keys create path/to/your/credentials.json \
     --iam-account=$IAM_ACCOUNT
   ```

   > **(*)** *Note:* The **Role** field authorizes your service account to access resources.
   > You can view and change this field later by using the
   > [GCP Console IAM page](https://console.cloud.google.com/iam-admin/iam).
   > If you are developing a production app, specify more granular permissions than **Project > Owner**.
   > For more information, see
   > [Granting roles to service accounts](https://cloud.google.com/iam/docs/granting-roles-to-service-accounts).

   For more information, see
   [Creating and managing service accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

1. Set your `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ```

## Setting up a Python development environment

For instructions on how to install Python, virtualenv, and the Cloud SDK, see the
[Setting up a Python development environment](https://cloud.google.com/python/setup)
guide.
