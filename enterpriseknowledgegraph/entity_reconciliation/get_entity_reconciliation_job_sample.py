# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# [START enterpriseknowledgegraph_get_entity_reconciliation_job]

from google.cloud import enterpriseknowledgegraph as ekg

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_GRAPH_LOCATION'  # Values: 'global'
# job_id = 'YOUR_JOB_ID'            # Entity Reconciliation Job ID


def get_entity_reconciliation_job_sample(
    project_id: str, location: str, job_id: str
) -> None:
    # Create a client
    client = ekg.EnterpriseKnowledgeGraphServiceClient()

    # The full resource name of the job
    # e.g. projects/{project_id}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}
    name = client.entity_reconciliation_job_path(
        project=project_id, location=location, entity_reconciliation_job=job_id
    )

    # Initialize request argument(s)
    request = ekg.GetEntityReconciliationJobRequest(name=name)

    # Make the request
    response = client.get_entity_reconciliation_job(request=request)

    print(f"Job: {response.name}")
    print(
        f"Input Table: {response.input_config.bigquery_input_configs[0].bigquery_table}"
    )
    print(f"Output Dataset: {response.output_config.bigquery_dataset}")
    print(f"State: {response.state.name}")


# [END enterpriseknowledgegraph_get_entity_reconciliation_job]
