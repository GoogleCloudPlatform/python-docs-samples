#!/usr/bin/env python

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START dataproc_quickstart]
"""
Command-line program to create a Dataproc cluster,
run a PySpark job located in Cloud Storage on the cluster,
then delete the cluster after the job completes.

Usage:
    python submit_job_to_cluster --project_id <PROJECT_ID> --region <REGION> \
        --cluster_name <CLUSTER_NAME> --job_file_path <GCS_JOB_FILE_PATH>
"""

import argparse
import os
import re

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


# [START dataproc_create_cluster]
def quickstart(project_id, region, cluster_name, gcs_bucket, pyspark_file):
    # Create the cluster client.
    cluster_client = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    # Create the cluster config.
    cluster = {
        "project_id": project_id,
        "cluster_name": cluster_name,
        "config": {
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
            "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
        },
    }

    # Create the cluster.
    operation = cluster_client.create_cluster(
        request={"project_id": project_id, "region": region, "cluster": cluster}
    )
    result = operation.result()

    print("Cluster created successfully: {}".format(result.cluster_name))

# [END dataproc_create_cluster]

    spark_file, spark_filename = get_pyspark_file(pyspark_file)
    upload_pyspark_file(project_id, gcs_bucket, spark_filename, spark_file)

# [START dataproc_submit_job]
    # Create the job client.
    job_client = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    # Create the job config.
    job = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {"main_python_file_uri": "gs://{}/{}".format(gcs_bucket, spark_filename)},
    }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    response = operation.result()

    # Dataproc job output is saved to the Cloud Storage bucket
    # allocated to the job. Use regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_string()
    )

    print(f"Job finished successfully: {output}\r\n")
    # [END dataproc_submit_job]

    # [START dataproc_delete_cluster]
    # Delete the cluster once the job has terminated.
    operation = cluster_client.delete_cluster(
        request={
            "project_id": project_id,
            "region": region,
            "cluster_name": cluster_name,
        }
    )
    operation.result()

    print("Cluster {} successfully deleted.".format(cluster_name))
# [END dataproc_delete_cluster]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project_id",
        type=str,
        required=True,
        help="Project to use for creating resources.",
    )
    parser.add_argument(
        "--region",
        type=str,
        required=True,
        help="Region where the resources should live.",
    )
    parser.add_argument(
        "--cluster_name",
        type=str,
        required=True,
        help="Name to use for creating a cluster.",
    )

    parser.add_argument(
        "--gcs_bucket", help="Bucket to upload Pyspark file to", required=True
    )

    parser.add_argument(
        "--pyspark_file", help="Pyspark filename. Defaults to pyspark_sort.py"
    )

    args = parser.parse_args()
    quickstart(args.project_id, args.region, args.cluster_name, args.gcs_bucket, args.pyspark_file)
# [END dataproc_quickstart]
