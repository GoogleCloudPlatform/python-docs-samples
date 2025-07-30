#!/usr/bin/env python

# Copyright 2025 Google LLC
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

# This sample walks a user through submitting a Spark job to a
# Dataproc driver node group cluster using the Dataproc
# client library.

# Usage:
#    python submit_spark_job_to_driver_node_group_cluster.py \
#        --project_id <PROJECT_ID> --region <REGION> \
#        --cluster_name <CLUSTER_NAME>

# [START dataproc_submit_spark_job_to_driver_node_group_cluster]

import re

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage


def submit_job(project_id: str, region: str, cluster_name: str) -> None:
    """Submits a Spark job to the specified Dataproc cluster with a driver node group and prints the output.

    Args:
        project_id: The Google Cloud project ID.
        region: The Dataproc region where the cluster is located.
        cluster_name: The name of the Dataproc cluster.
    """
    # Create the job client.
    with dataproc.JobControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    ) as job_client:

        driver_scheduling_config = dataproc.DriverSchedulingConfig(
            memory_mb=2048,  # Example memory in MB
            vcores=2,  # Example number of vcores
        )

        # Create the job config. 'main_jar_file_uri' can also be a
        # Google Cloud Storage URL.
        job = {
            "placement": {"cluster_name": cluster_name},
            "spark_job": {
                "main_class": "org.apache.spark.examples.SparkPi",
                "jar_file_uris": ["file:///usr/lib/spark/examples/jars/spark-examples.jar"],
                "args": ["1000"],
            },
            "driver_scheduling_config": driver_scheduling_config
        }

        operation = job_client.submit_job_as_operation(
            request={"project_id": project_id, "region": region, "job": job}
        )

        response = operation.result()

        # Dataproc job output gets saved to the Cloud Storage bucket
        # allocated to the job. Use a regex to obtain the bucket and blob info.
        matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)
        if not matches:
            print(f"Error: Could not parse driver output URI: {response.driver_output_resource_uri}")
            raise ValueError

        output = (
            storage.Client()
            .get_bucket(matches.group(1))
            .blob(f"{matches.group(2)}.000000000")
            .download_as_bytes()
            .decode("utf-8")
        )

        print(f"Job finished successfully: {output}")

# [END dataproc_submit_spark_job_to_driver_node_group_cluster]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Submits a Spark job to a Dataproc driver node group cluster."
    )
    parser.add_argument("--project_id", help="The Google Cloud project ID.", required=True)
    parser.add_argument("--region", help="The Dataproc region where the cluster is located.", required=True)
    parser.add_argument("--cluster_name", help="The name of the Dataproc cluster.", required=True)

    args = parser.parse_args()
    submit_job(args.project_id, args.region, args.cluster_name)
