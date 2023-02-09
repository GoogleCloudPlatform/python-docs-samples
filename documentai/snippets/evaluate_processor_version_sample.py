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

# [START documentai_evaluate_processor_version]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1beta3 as documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID'
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'
# gcs_input_uri = # Format: gs://bucket/directory/


def evaluate_processor_version_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version_id: str,
    gcs_input_uri: str,
):
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g. `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    evaluation_documents = documentai.BatchDocumentsInputConfig(
        gcs_prefix=documentai.GcsPrefix(gcs_uri_prefix=gcs_input_uri)
    )

    # NOTE: Alternatively, specify a list of GCS Documents
    #
    # gcs_input_uri = "gs://bucket/directory/file.pdf"
    # input_mime_type = "application/pdf"
    #
    # gcs_document = documentai.GcsDocument(
    #     gcs_uri=gcs_input_uri, mime_type=input_mime_type
    # )
    # gcs_documents = [gcs_document]
    # evaluation_documents = documentai.BatchDocumentsInputConfig(
    #     gcs_documents=documentai.GcsDocuments(documents=gcs_documents)
    # )
    #

    request = documentai.EvaluateProcessorVersionRequest(
        processor_version=name,
        evaluation_documents=evaluation_documents,
    )

    # Make EvaluateProcessorVersion request
    # Continually polls the operation until it is complete.
    # This could take some time for larger files
    operation = client.evaluate_processor_version(request=request)
    # Print operation details
    # Format: projects/PROJECT_NUMBER/locations/LOCATION/operations/OPERATION_ID
    print(f"Waiting for operation {operation.operation.name} to complete...")
    # Wait for operation to complete
    response = documentai.EvaluateProcessorVersionResponse(operation.result())

    # Once the operation is complete,
    # Print evaluation ID from operation response
    print(f"Evaluation Complete: {response.evaluation}")


# [END documentai_evaluate_processor_version]
