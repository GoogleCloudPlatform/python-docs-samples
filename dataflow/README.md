# Getting started with Google Cloud Dataflow

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/README.md)

[Apache Beam](https://beam.apache.org/)
is an open source, unified model for defining both batch and streaming data-parallel processing pipelines.
This guides you through all the steps needed to run an Apache Beam pipeline in the
[Google Cloud Dataflow](https://cloud.google.com/dataflow) runner.

## Setting up your Google Cloud project

The following instructions help you prepare your Google Cloud project.

1. Install the [Cloud SDK](https://cloud.google.com/sdk/docs/).

   > ℹ️ This is not required in
   > [Cloud Shell](https://console.cloud.google.com/cloudshell/editor)
   > since it already has the Cloud SDK pre-installed.

1. Create a new Google Cloud project and save the project ID in an environment variable.

   <button><a href="https://console.cloud.google.com/projectcreate">
      Click here to create a new project
   </a></button>

   ```sh
   # Save your project ID in an environment variable for ease of use later on.
   export PROJECT=your-google-cloud-project-id
   ```

1. Setup the Cloud SDK to your GCP project.

   ```sh
   gcloud init
   ```

1. [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project).

1. Enable the Dataflow API.

   <button><a href="https://console.cloud.google.com/flows/enableapi?apiid=dataflow">
      Click here to enable the API
   </a></button>

1. Authenticate to your Google Cloud project.

   ```sh
   gcloud auth application-default login
   ```

   > ℹ️ For more information on authentication, see the
   > [Authentication overview](https://googleapis.dev/python/google-api-core/latest/auth.html) page.
   >
   > To learn more about the permissions needed for Dataflow, see the
   > [Dataflow security and permissions](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions) page.

## Setting up a Python development environment

For instructions on how to install Python, virtualenv, and the Cloud SDK, see the
[Setting up a Python development environment](https://cloud.google.com/python/setup)
guide.
