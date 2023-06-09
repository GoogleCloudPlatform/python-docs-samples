#!/usr/bin/env python

# Copyright 2020 Google LLC
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

# This sample walks a user through submitting a Spark job using the Dataproc
# client library.

# Usage:
#    python submit_job.py --project_id <PROJECT_ID> --region <REGION> \
#        --cluster_name <CLUSTER_NAME>

# [START dataproc_submit_job]
import re

# [END dataproc_submit_job]
import sys

# [START dataproc_submit_job]

from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage


def submit_job(project_id, region, cluster_name):
    # Create the job client.
    job_client = dataproc.JobControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
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
    }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    response = operation.result()

    # Dataproc job output gets saved to the Google Cloud Storage bucket
    # allocated to the job. Use a regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_bytes().decode("utf-8")
    )

    print(f"Job finished successfully: {output}")


# [END dataproc_submit_job]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("python submit_job.py project_id region cluster_name")

    project_id = sys.argv[1]
    region = sys.argv[2]
    cluster_name = sys.argv[3]
    submit_job(project_id, region, cluster_name)
