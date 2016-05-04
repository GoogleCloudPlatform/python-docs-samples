# Transfer Service sample using Python

This app creates two types of transfers using the Transfer Service tool.

<!-- auto-doc-link -->
These samples are used on the following documentation pages:

>
* https://cloud.google.com/storage/transfer/create-client
* https://cloud.google.com/storage/transfer/create-manage-transfer-program

<!-- end-auto-doc-link -->

## Prerequisites

1. Set up a project on Google Developers Console.
  1. Go to the [Developers Console](https://cloud.google.com/console) and create or select your project.
     You will need the project ID later.
1. Within Developers Console, select APIs & auth > Credentials.
  1. Select Add credentials > Service account > JSON key.
  1. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to point to your JSON key.
1. Add the Storage Transfer service account as an editor of your project
   storage-transfer-<accountId>@partnercontent.gserviceaccount.com
1. Set up gcloud for application default credentials.
  1. `gcloud components update`
  1. `gcloud init`
1. Install [Google API Client Library for Python](https://developers.google.com/api-client-library/python/start/installation).

## Transfer from Amazon S3 to Google Cloud Storage

Creating a one-time transfer from Amazon S3 to Google Cloud Storage.
1. Set up data sink.
  1. Go to the Developers Console and create a bucket under Cloud Storage > Storage Browser.
1. Set up data source.
  1. Go to AWS Management Console and create a bucket.
  1. Under Security Credentials, create an IAM User with access to the bucket.
  1. Create an Access Key for the user. Note the Access Key ID and Secret Access Key.
1. In aws_request.py, fill in the Transfer Job JSON template with relevant values.
1. Run with `python aws_request.py`
  1. Note the job ID in the returned Transfer Job.

## Transfer data from a standard Cloud Storage bucket to a Cloud Storage Nearline bucket

Creating a daily transfer from a standard Cloud Storage bucket to a Cloud Storage Nearline
bucket for files untouched for 30 days.
1. Set up data sink.
  1. Go to the Developers Console and create a bucket under Cloud Storage > Storage Browser.
  1. Select Nearline for Storage Class.
1. Set up data source.
  1. Go to the Developers Console and create a bucket under Cloud Storage > Storage Browser.
1. In nearline_request.py, fill in the Transfer Job JSON template with relevant values.
1. Run with `python nearline_request.py`
  1. Note the job ID in the returned Transfer Job.

## Checking the status of a transfer

1. In transfer_check.py, fill in the Transfer Job JSON template with relevant values.
   Use the Job Name you recorded earlier.
1. Run with `python transfer_check.py`
