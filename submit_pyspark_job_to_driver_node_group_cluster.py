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
#    python submit_pyspark_job_to_driver_node_group_cluster.py \
#        --project_id <PROJECT_ID> --region <REGION> \
#        --cluster_name <CLUSTER_NAME>

# [START dataproc_submit_pyspark_job_to_driver_node_group_cluster]

import re
 
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage


def submit_job(project_id, region, cluster_name):
    """Submits a PySpark job to a Dataproc cluster with a driver node group.

    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the Dataproc cluster is located.
        cluster_name (str): The name of the Dataproc cluster.
    """
    # Create the job client.
    job_client = dataproc.JobControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )
 
    driver_scheduling_config = dataproc.DriverSchedulingConfig(
    memory_mb=2048, # Example memory in MB
    vcores=2, # Example number of vcores
    )
 
    # Create the job config. 'main_python_file_uri' can also be a
    # Google Cloud Storage URL.
    job = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": "gs://dataproc-examples/pyspark/hello-world/hello-world.py"
        },
        "driver_scheduling_config": driver_scheduling_config
    }
 
    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    response = operation.result()
 
    # Dataproc job output gets saved to the Google Cloud Storage bucket
    # allocated to the job. Use a regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)
    if not matches:
        raise ValueError(f"Unexpected driver output URI: {response.driver_output_resource_uri}")
 
    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_bytes()
        .decode("utf-8")
    )
 
    print(f"Job finished successfully: {output}")

# [END dataproc_submit_pyspark_job_to_driver_node_group_cluster]

if __name__ == "__main__":
 
    my_project_id = "your_project_id"  # <-- REPLACE THIS
    my_region = "your_region"        # <-- REPLACE THIS
    my_cluster_name = "your_node_group_cluster" # <-- REPLACE THIS
 
    submit_job(my_project_id, my_region, my_cluster_name)
