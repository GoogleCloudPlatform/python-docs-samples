# Use the Python Client Library to call Cloud Dataproc APIs

Estimated completion time: <walkthrough-tutorial-duration duration="5"></walkthrough-tutorial-duration>

## Overview

This [Cloud Shell](https://cloud.google.com/shell/docs/) walkthrough leads you
through the steps to use the
[Google Cloud Client Libraries for Python](https://googleapis.github.io/google-cloud-python/latest/dataproc/index.html)
to programmatically interact with [Cloud Dataproc](https://cloud.google.com/dataproc/docs/).

As you follow this walkthrough, you run Python code that calls
[Cloud Dataproc gRPC APIs](https://cloud.google.com/dataproc/docs/reference/rpc/)
to:

* create a Cloud Dataproc cluster
* submit a small PySpark word sort job to run on the cluster
* get job status
* tear down the cluster after job completion

## Using the walkthrough

The `submit_job_to_cluster.py file` used in this walkthrough is opened in the
Cloud Shell editor when you launch the walkthrough. You can view
the code as your follow the walkthrough steps.

**For more information**: See [Cloud Dataproc&rarr;Use the Python Client Library](https://cloud.google.com/dataproc/docs/tutorials/python-library-example) for
an explanation of how the code works.

**To reload this walkthrough:** Run the following command from the
`~/python-docs-samples/dataproc` directory in Cloud Shell:

    cloudshell launch-tutorial python-api-walkthrough.md

**To copy and run commands**: Click the "Paste in Cloud Shell" button
  (<walkthrough-cloud-shell-icon></walkthrough-cloud-shell-icon>)
  on the side of a code box, then press `Enter` to run the command.

## Prerequisites (1)

1. Create or select a Google Cloud Platform project to use for this tutorial.
    * <walkthrough-project-billing-setup permissions=""></walkthrough-project-billing-setup>

1. Enable the Cloud Dataproc, Compute Engine, and Cloud Storage APIs in your project.
    * <walkthrough-enable-apis apis="dataproc,compute_component,storage-component.googleapis.com"></walkthrough-enable-apis>

## Prerequisites (2)

1. This walkthrough uploads a PySpark file (`pyspark_sort.py`) to a
   [Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets) in
   your project.
   * You can use the [Cloud Storage browser page](https://console.cloud.google.com/storage/browser)
   in Google Cloud Platform Console to view existing buckets in your project.

   &nbsp;&nbsp;&nbsp;&nbsp;**OR**

   * To create a new bucket, run the following command. Your bucket name must be unique.
   ```bash
   gsutil mb -p {{project-id}} gs://your-bucket-name
   ```

1.  Set environment variables.

    * Set the name of your bucket.
    ```bash
    BUCKET=your-bucket-name
    ```

## Prerequisites (3)

1. Set up a Python
   [virtual environment](https://virtualenv.readthedocs.org/en/latest/)
   in Cloud Shell.

    * Create the virtual environment.
    ```bash
    virtualenv ENV
    ```
    * Activate the virtual environment.
    ```bash
    source ENV/bin/activate
    ```

1. Install library dependencies in Cloud Shell.
    ```bash
    pip install -r requirements.txt
    ```

## Create a cluster and submit a job

1. Set a name for your new cluster.
    ```bash
    CLUSTER=new-cluster-name
    ```

1. Set a [zone](https://cloud.google.com/compute/docs/regions-zones/#available)
   where your new cluster will be located. You can change the
   "us-central1-a" zone that is pre-set in the following command.
    ```bash
    ZONE=us-central1-a
    ```

1. Run `submit_job.py` with the `--create_new_cluster` flag
   to create a new cluster and submit the `pyspark_sort.py` job
   to the cluster.

    ```bash
    python submit_job_to_cluster.py \
    --project_id={{project-id}} \
    --cluster_name=$CLUSTER \
    --zone=$ZONE \
    --gcs_bucket=$BUCKET \
    --create_new_cluster
    ```

## Job Output

Job output in Cloud Shell shows cluster creation, job submission,
    job completion, and then tear-down of the cluster.

     ...
     Creating cluster...
     Cluster created.
     Uploading pyspark file to Cloud Storage.
     new-cluster-name - RUNNING
     Submitted job ID ...
     Waiting for job to finish...
     Job finished.
     Downloading output file
     .....
     ['Hello,', 'dog', 'elephant', 'panther', 'world!']
     ...
     Tearing down cluster
     ```
## Congratulations on Completing the Walkthrough!
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

---

### Next Steps:

* **View job details from the Console.** View job details by selecting the
   PySpark job from the Cloud Dataproc
   [Jobs page](https://console.cloud.google.com/dataproc/jobs)
   in the Google Cloud Platform Console.

* **Delete resources used in the walkthrough.**
   The `submit_job_to_cluster.py` job deletes the cluster that it created for this
   walkthrough.

   If you created a bucket to use for this walkthrough,
   you can run the following command to delete the
   Cloud Storage bucket (the bucket must be empty).
   ```bash
   gsutil rb gs://$BUCKET
   ```
   You can run the following command to delete the bucket **and all
   objects within it. Note: the deleted objects cannot be recovered.**
   ```bash
   gsutil rm -r gs://$BUCKET
   ```

* **For more information.** See the [Cloud Dataproc documentation](https://cloud.google.com/dataproc/docs/)
   for API reference and product feature information.
