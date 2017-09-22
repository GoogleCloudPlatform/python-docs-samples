# Cloud Dataproc API Example

Sample command-line programs for interacting with the Cloud Dataproc API.

Note that while this sample demonstrates interacting with Dataproc via the API, the functionality
demonstrated here could also be accomplished using the Cloud Console or the gcloud CLI.

`list_clusters.py` is a simple command-line program to demonstrate connecting to the
Dataproc API and listing the clusters in a region

`create_cluster_and_submit_job.py` demonstrates how to create a cluster, submit the 
`pyspark_sort.py` job, download the output from Google Cloud Storage, and output the result.

## Prerequisites to run locally:

* [pip](https://pypi.python.org/pypi/pip)

Go to the [Google Cloud Console](https://console.cloud.google.com).

Under API Manager, search for the Google Cloud Dataproc API and enable it.


# Set Up Your Local Dev Environment
To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

    * pip install -r requirements.txt

Create local credentials by running the following command and following the oauth2 flow:

    gcloud beta auth application-default login

To run list_clusters.py:

    python list_clusters.py <YOUR-PROJECT-ID> --region=us-central1


To run submit_job_to_cluster.py, first create a GCS bucket, from the Cloud Console or with
gsutil:

    gsutil mb gs://<your-input-bucket-name>
    
Then, if you want to rely on an existing cluster, run:
    
    python submit_job_to_cluster.py --project_id=<your-project-id> --zone=us-central1-b --cluster_name=testcluster --gcs_bucket=<your-input-bucket-name>
    
Otherwise, if you want the script to create a new cluster for you:

    python submit_job_to_cluster.py --project_id=<your-project-id> --zone=us-central1-b --cluster_name=testcluster --gcs_bucket=<your-input-bucket-name> --create_new_cluster


This will setup a cluster, upload the PySpark file, submit the job, print the result, then
delete the cluster.

You can optionally specify a `--pyspark_file` argument to change from the default 
`pyspark_sort.py` included in this script to a new script.

## Running on GCE, GAE, or other environments

On Google App Engine, the credentials should be found automatically.

On Google Compute Engine, the credentials should be found automatically, but require that
you create the instance with the correct scopes. 

    gcloud compute instances create --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/compute.readonly" test-instance

If you did not create the instance with the right scopes, you can still upload a JSON service 
account and set `GOOGLE_APPLICATION_CREDENTIALS`. See [Google Application Default Credentials](https://developers.google.com/identity/protocols/application-default-credentials) for more details.
