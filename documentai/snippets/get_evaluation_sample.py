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

# [START documentai_get_evaluation]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1beta3 as documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'
# evaluation_id = 'YOUR_EVALUATION_ID'


def get_evaluation_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version_id: str,
    evaluation_id: str,
):
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the evaluation
    # e.g. `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    evaluation_name = client.evaluation_path(
        project_id, location, processor_id, processor_version_id, evaluation_id
    )
    # Make GetEvaluation request
    evaluation = client.get_evaluation(name=evaluation_name)

    create_time = evaluation.create_time
    document_counters = evaluation.document_counters

    # Print the Evaluation Information
    # Refer to https://cloud.google.com/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions.evaluations
    # for more information on the available evaluation data
    print(f"Create Time: {create_time}")
    print(f"Input Documents: {document_counters.input_documents_count}")
    print(f"\tInvalid Documents: {document_counters.invalid_documents_count}")
    print(f"\tFailed Documents: {document_counters.failed_documents_count}")
    print(f"\tEvaluated Documents: {document_counters.evaluated_documents_count}")


# [END documentai_get_evaluation]
