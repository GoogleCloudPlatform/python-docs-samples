#!/usr/bin/env python

# Copyright 2019 Google LLC
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

r"""Sample Cloud Dataproc inline workflow to run a pyspark job on an ephermeral
cluster.
Example Usage to run the inline workflow on a managed cluster:
python single_job_workflow.py --project_id=$PROJECT --gcs_bucket=$BUCKET \
  --cluster_name=$CLUSTER --zone=$ZONE
Example Usage to run the inline workflow on a global region managed cluster:
python submit_job_to_cluster.py --project_id=$PROJECT --gcs_bucket=$BUCKET \
  --cluster_name=$CLUSTER --zone=$ZONE --global_region
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

from google.cloud import dataproc_v1
from google.cloud import storage
from google.cloud.dataproc_v1.gapic.transports import (
    workflow_template_service_grpc_transport,
)


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


def run_workflow(dataproc, project, region, zone, bucket_name, filename, cluster_name):

    parent = "projects/{}/regions/{}".format(project, region)
    zone_uri = "https://www.googleapis.com/compute/v1/projects/{}/zones/{}".format(
        project, zone
    )

    workflow_data = {
        "placement": {
            "managed_cluster": {
                "cluster_name": cluster_name,
                "config": {
                    "gce_cluster_config": {"zone_uri": zone_uri},
                    "master_config": {
                        "num_instances": 1,
                        "machine_type_uri": "n1-standard-1",
                    },
                    "worker_config": {
                        "num_instances": 2,
                        "machine_type_uri": "n1-standard-1",
                    },
                },
            }
        },
        "jobs": [
            {
                "pyspark_job": {
                    "main_python_file_uri": "gs://{}/{}".format(bucket_name, filename)
                },
                "step_id": "pyspark-job",
            }
        ],
    }

    workflow = dataproc.instantiate_inline_workflow_template(
        request={"parent": parent, "template": workflow_data}
    )

    workflow.add_done_callback(callback)
    global waiting_callback
    waiting_callback = True


def callback(operation_future):
    # Reset global when callback returns.
    global waiting_callback
    waiting_callback = False


def wait_for_workflow_end():
    """Wait for cluster creation."""
    print("Waiting for workflow completion ...")
    print(
        "Workflow and job progress, and job driver output available from: "
        "https://console.cloud.google.com/dataproc/workflows/"
    )

    while True:
        if not waiting_callback:
            print("Workflow completed.")
            break


def main(
    project_id,
    zone,
    cluster_name,
    bucket_name,
    pyspark_file=None,
    create_new_cluster=True,
    global_region=True,
):

    # [START dataproc_get_workflow_template_client]
    if global_region:
        region = "global"
        # Use the default gRPC global endpoints.
        dataproc_workflow_client = dataproc_v1.WorkflowTemplateServiceClient()
    else:
        region = get_region_from_zone(zone)
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        client_transport = workflow_template_service_grpc_transport.WorkflowTemplateServiceGrpcTransport(
            address="{}-dataproc.googleapis.com:443".format(region)
        )
        dataproc_workflow_client = dataproc_v1.WorkflowTemplateServiceClient(
            client_transport
        )
    # [END dataproc_get_workflow_template_client]

    try:
        spark_file, spark_filename = get_pyspark_file(pyspark_file)
        upload_pyspark_file(project_id, bucket_name, spark_filename, spark_file)

        run_workflow(
            dataproc_workflow_client,
            project_id,
            region,
            zone,
            bucket_name,
            spark_filename,
            cluster_name,
        )
        wait_for_workflow_end()

    finally:
        spark_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=(argparse.RawDescriptionHelpFormatter)
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
    )
