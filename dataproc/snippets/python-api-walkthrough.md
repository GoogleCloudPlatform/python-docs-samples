# Use the Python Client Library to call Dataproc APIs

Estimated completion time: <walkthrough-tutorial-duration duration="5"></walkthrough-tutorial-duration>

## Overview

This [Cloud Shell](https://cloud.google.com/shell/docs/) walkthrough leads you
through the steps to use the
[Cloud Client Libraries for Python](https://googleapis.github.io/google-cloud-python/latest/dataproc/index.html)
to programmatically interact with [Dataproc](https://cloud.google.com/dataproc/docs/).

As you follow this walkthrough, you run Python code that calls
[Dataproc gRPC APIs](https://cloud.google.com/dataproc/docs/reference/rpc/)
to:

* Create a Dataproc cluster
* Submit a PySpark word sort job to the cluster
* Delete the cluster after job completion

## Using the walkthrough

The `submit_job_to_cluster.py file` used in this walkthrough is opened in the
Cloud Shell editor when you launch the walkthrough. You can view
the code as your follow the walkthrough steps.

**For more information**: See [Use the Cloud Client Libraries for Python](https://cloud.google.com/dataproc/docs/tutorials/python-library-example) for
an explanation of how the code works.

**To reload this walkthrough:** Run the following command from the
`~/python-docs-samples/dataproc` directory in Cloud Shell:

    cloudshell launch-tutorial python-api-walkthrough.md

**To copy and run commands**: Click the "Copy to Cloud Shell" button
  (<walkthrough-cloud-shell-icon></walkthrough-cloud-shell-icon>)
  on the side of a code box, then press `Enter` to run the command.

## Prerequisites (1)

<walkthrough-watcher-constant key="project_id" value="<project_id>"></walkthrough-watcher-constant>

1. Create or select a Google Cloud project to use for this
   tutorial.
   * <walkthrough-project-setup billing="true"></walkthrough-project-setup>

1. Enable the Dataproc, Compute Engine, and Cloud Storage APIs in your
   project.
 
    ```bash
    gcloud services enable dataproc.googleapis.com \
    compute.googleapis.com \
    storage-component.googleapis.com \
    --project={{project_id}}
    ```

## Prerequisites (2)

1. This walkthrough uploads a PySpark file (`pyspark_sort.py`) to a
   [Cloud Storage bucket](https://cloud.google.com/storage/docs/key-terms#buckets) in
   your project.
   * You can use the [Cloud Storage browser page](https://console.cloud.google.com/storage/browser)
     in Google Cloud Console to view existing buckets in your project.

     **OR**

   * To create a new bucket, run the following command. Your bucket name must be unique.

         gsutil mb -p {{project-id}} gs://your-bucket-name
    

2. Set environment variables.
   * Set the name of your bucket.
    
         BUCKET=your-bucket-name

## Prerequisites (3)

1. Set up a Python
   [virtual environment](https://virtualenv.readthedocs.org/en/latest/).

    * Create the virtual environment.

          virtualenv ENV

    * Activate the virtual environment.
    
          source ENV/bin/activate

1. Install library dependencies.

          pip install -r requirements.txt

## Create a cluster and submit a job

1. Set a name for your new cluster.

         CLUSTER=new-cluster-name

1. Set a [region](https://cloud.google.com/compute/docs/regions-zones/#available)
   where your new cluster will be located. You can change the pre-set
   "us-central1" region beforew you copy and run the following command.

         REGION=us-central1

1. Run `submit_job_to_cluster.py` to create a new cluster and run the
   `pyspark_sort.py` job on the cluster.

         python submit_job_to_cluster.py \
         --project_id={{project-id}} \
         --region=$REGION \
         --cluster_name=$CLUSTER \
         --gcs_bucket=$BUCKET

## Job Output

Job output displayed in the Cloud Shell terminaL shows cluster creation,
job completion, sorted job output, and then deletion of the cluster.

```xml
Cluster created successfully: cliuster-name.
...
Job finished successfully.
...
['Hello,', 'dog', 'elephant', 'panther', 'world!']
...
Cluster cluster-name successfully deleted.
```

## Congratulations on completing the Walkthrough!
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

---

### Next Steps:

* **View job details in the Cloud Console.** View job details by selecting the
   PySpark job name on the Dataproc 
   [Jobs page](https://console.cloud.google.com/dataproc/jobs)
   in the Cloud console.

* **Delete resources used in the walkthrough.**
   The `submit_job_to_cluster.py` code deletes the cluster that it created for this
   walkthrough.

   If you created a Cloud Storage bucket to use for this walkthrough,
   you can run the following command to delete the bucket (the bucket must be empty).

         gsutil rb gs://$BUCKET

   * You can run the following command to **delete the bucket and all
     objects within it. Note: the deleted objects cannot be recovered.**

         gsutil rm -r gs://$BUCKET
  

* **For more information.** See the [Dataproc documentation](https://cloud.google.com/dataproc/docs/)
   for API reference and product feature information.
