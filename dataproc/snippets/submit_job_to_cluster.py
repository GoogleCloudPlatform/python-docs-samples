#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Sample command-line program to run a pyspark job on a new or existing
cluster.

Global region clusters are supported with --global_region flag.

Example Usage to run the pyspark job on a new cluster:
python submit_job_to_cluster.py --project_id=$PROJECT --gcs_bucket=$BUCKET \
  --create_new_cluster --cluster_name=$CLUSTER --zone=$ZONE

Example Usage to run the pyspark job on an existing global region cluster:
python submit_job_to_cluster.py --project_id=$PROJECT --gcs_bucket=$BUCKET \
  --global_region --cluster_name=$CLUSTER --zone=$ZONE

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

from google.cloud import dataproc_v1
from google.cloud import storage


DEFAULT_FILENAME = "pyspark_sort.py"
waiting_callback = False


def get_pyspark_file(pyspark_file=None):
    if pyspark_file:
        f = open(pyspark_file, "rb")
        return f, os.path.basename(pyspark_file)
    else:
        """Gets the PySpark file from current directory."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(current_dir, DEFAULT_FILENAME), "rb")
        return f, DEFAULT_FILENAME


def get_region_from_zone(zone):
    try:
        region_as_list = zone.split("-")[:-1]
        return "-".join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError("Invalid zone provided, please check your input.")


def upload_pyspark_file(project, bucket_name, filename, spark_file):
    """Uploads the PySpark file in this directory to the configured input
    bucket."""
    print("Uploading pyspark file to Cloud Storage.")
    client = storage.Client(project=project)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(spark_file)


def download_output(project, cluster_id, output_bucket, job_id):
    """Downloads the output file from Cloud Storage and returns it as a
    string."""
    print("Downloading output file.")
    client = storage.Client(project=project)
    bucket = client.get_bucket(output_bucket)
    output_blob = "google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000".format(
        cluster_id, job_id
    )
    return bucket.blob(output_blob).download_as_string()


# [START dataproc_submit_job_create_cluster]
def create_cluster(dataproc, project, zone, region, cluster_name):
    """Create the cluster."""
    print("Creating cluster...")
    zone_uri = "https://www.googleapis.com/compute/v1/projects/{}/zones/{}".format(
        project, zone
    )
    cluster_data = {
        "project_id": project,
        "cluster_name": cluster_name,
        "config": {
            "gce_cluster_config": {"zone_uri": zone_uri},
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-1"},
            "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-1"},
        },
    }

    cluster = dataproc.create_cluster(
        request={"project_id": project, "region": region, "cluster": cluster_data}
    )
    cluster.add_done_callback(callback)
    global waiting_callback
    waiting_callback = True


# [END dataproc_submit_job_create_cluster]


def callback(operation_future):
    # Reset global when callback returns.
    global waiting_callback
    waiting_callback = False


def wait_for_cluster_creation():
    """Wait for cluster creation."""
    print("Waiting for cluster creation...")

    while True:
        if not waiting_callback:
            print("Cluster created.")
            break


# [START dataproc_list_clusters_with_detail]
def list_clusters_with_details(dataproc, project, region):
    """List the details of clusters in the region."""
    for cluster in dataproc.list_clusters(
        request={"project_id": project, "region": region}
    ):
        print(("{} - {}".format(cluster.cluster_name, cluster.status.state.name,)))


# [END dataproc_list_clusters_with_detail]


def get_cluster_id_by_name(dataproc, project_id, region, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    for cluster in dataproc.list_clusters(
        request={"project_id": project_id, "region": region}
    ):
        if cluster.cluster_name == cluster_name:
            return cluster.cluster_uuid, cluster.config.config_bucket


# [START dataproc_submit_pyspark_job]
def submit_pyspark_job(dataproc, project, region, cluster_name, bucket_name, filename):
    """Submit the Pyspark job to the cluster (assumes `filename` was uploaded
    to `bucket_name."""
    job_details = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": "gs://{}/{}".format(bucket_name, filename)
        },
    }

    result = dataproc.submit_job(
        request={"project_id": project, "region": region, "job": job_details}
    )
    job_id = result.reference.job_id
    print("Submitted job ID {}.".format(job_id))
    return job_id


# [END dataproc_submit_pyspark_job]


# [START dataproc_delete]
def delete_cluster(dataproc, project, region, cluster):
    """Delete the cluster."""
    print("Tearing down cluster.")
    result = dataproc.delete_cluster(
        request={"project_id": project, "region": region, "cluster_name": cluster}
    )
    return result


# [END dataproc_delete]


# [START dataproc_wait]
def wait_for_job(dataproc, project, region, job_id):
    """Wait for job to complete or error out."""
    print("Waiting for job to finish...")
    while True:
        job = dataproc.get_job(
            request={"project_id": project, "region": region, "job_id": job_id}
        )
        # Handle exceptions
        if job.status.State(job.status.state).name == "ERROR":
            raise Exception(job.status.details)
        if job.status.State(job.status.state).name == "DONE":
            print("Job finished.")
            return job


# [END dataproc_wait]


def main(
    project_id,
    zone,
    cluster_name,
    bucket_name,
    pyspark_file=None,
    create_new_cluster=True,
    global_region=True,
):

    # [START dataproc_get_client]
    if global_region:
        region = "global"
        # Use the default gRPC global endpoints.
        dataproc_cluster_client = dataproc_v1.ClusterControllerClient()
        dataproc_job_client = dataproc_v1.JobControllerClient()
    else:
        region = get_region_from_zone(zone)
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        dataproc_cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
        )
        dataproc_job_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
        )
    # [END dataproc_get_client]

    try:
        spark_file, spark_filename = get_pyspark_file(pyspark_file)
        if create_new_cluster:
            create_cluster(
                dataproc_cluster_client, project_id, zone, region, cluster_name
            )
            wait_for_cluster_creation()
        upload_pyspark_file(project_id, bucket_name, spark_filename, spark_file)

        list_clusters_with_details(dataproc_cluster_client, project_id, region)

        (cluster_id, output_bucket) = get_cluster_id_by_name(
            dataproc_cluster_client, project_id, region, cluster_name
        )

        # [START dataproc_call_submit_pyspark_job]
        job_id = submit_pyspark_job(
            dataproc_job_client,
            project_id,
            region,
            cluster_name,
            bucket_name,
            spark_filename,
        )
        # [END dataproc_call_submit_pyspark_job]

        wait_for_job(dataproc_job_client, project_id, region, job_id)
        output = download_output(project_id, cluster_id, output_bucket, job_id)
        print("Received job output {}".format(output))
        return output
    finally:
        if create_new_cluster:
            delete_cluster(dataproc_cluster_client, project_id, region, cluster_name)
            spark_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--project_id", help="Project ID you want to access.", required=True
    )
    parser.add_argument(
        "--zone", help="Zone to create clusters in/connect to", required=True
    )
    parser.add_argument(
        "--cluster_name", help="Name of the cluster to create/connect to", required=True
    )
    parser.add_argument(
        "--gcs_bucket", help="Bucket to upload Pyspark file to", required=True
    )
    parser.add_argument(
        "--pyspark_file", help="Pyspark filename. Defaults to pyspark_sort.py"
    )
    parser.add_argument(
        "--create_new_cluster",
        action="store_true",
        help="States if the cluster should be created",
    )
    parser.add_argument(
        "--global_region",
        action="store_true",
        help="If cluster is in the global region",
    )

    args = parser.parse_args()
    main(
        args.project_id,
        args.zone,
        args.cluster_name,
        args.gcs_bucket,
        args.pyspark_file,
        args.create_new_cluster,
        args.global_region,
    )
