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

# This sample walks a user through instantiating an inline
# workflow for Cloud Dataproc using the Python client library.
#
# This script can be run on its own:
#   python instantiate_inline_workflow_template.py ${PROJECT_ID} ${REGION}


import sys

# [START dataproc_instantiate_inline_workflow_template]
from google.cloud import dataproc_v1 as dataproc


def instantiate_inline_workflow_template(project_id, region):
    """This sample walks a user through submitting a workflow
    for a Cloud Dataproc using the Python client library.

    Args:
        project_id (string): Project to use for running the workflow.
        region (string): Region where the workflow resources should live.
    """

    # Create a client with the endpoint set to the desired region.
    workflow_template_client = dataproc.WorkflowTemplateServiceClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )

    parent = "projects/{}/regions/{}".format(project_id, region)

    template = {
        "jobs": [
            {
                "hadoop_job": {
                    "main_jar_file_uri": "file:///usr/lib/hadoop-mapreduce/"
                    "hadoop-mapreduce-examples.jar",
                    "args": ["teragen", "1000", "hdfs:///gen/"],
                },
                "step_id": "teragen",
            },
            {
                "hadoop_job": {
                    "main_jar_file_uri": "file:///usr/lib/hadoop-mapreduce/"
                    "hadoop-mapreduce-examples.jar",
                    "args": ["terasort", "hdfs:///gen/", "hdfs:///sort/"],
                },
                "step_id": "terasort",
                "prerequisite_step_ids": ["teragen"],
            },
        ],
        "placement": {
            "managed_cluster": {
                "cluster_name": "my-managed-cluster",
                "config": {
                    "gce_cluster_config": {
                        # Leave 'zone_uri' empty for 'Auto Zone Placement'
                        # 'zone_uri': ''
                        "zone_uri": "us-central1-a"
                    }
                },
            }
        },
    }

    # Submit the request to instantiate the workflow from an inline template.
    operation = workflow_template_client.instantiate_inline_workflow_template(
        request={"parent": parent, "template": template}
    )
    operation.result()

    # Output a success message.
    print("Workflow ran successfully.")
    # [END dataproc_instantiate_inline_workflow_template]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(
            "python instantiate_inline_workflow_template.py " + "project_id region"
        )

    project_id = sys.argv[1]
    region = sys.argv[2]
    instantiate_inline_workflow_template(project_id, region)
