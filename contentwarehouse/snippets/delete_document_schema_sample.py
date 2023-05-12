# Copyright 2023 Google LLC
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


# [START contentwarehouse_delete_document_schema]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# document_schema_id = "YOUR_DOCUMENT SCHEMA_ID"


def sample_delete_document_schema(
    project_number: str,
    location: str,
    document_schema_id: str
) -> None:
    """Deletes document schema.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        document_schema_id: Unique identifier for document schema
    """
    # Create a client
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}
    document_schema_path = document_schema_client.document_schema_path(
        project=project_number,
        location=location,
        document_schema=document_schema_id,
    )

    # Initialize request argument(s)
    request = contentwarehouse.DeleteDocumentSchemaRequest(
        name=document_schema_path,
    )

    # Make the request
    response = document_schema_client.delete_document_schema(
        request=request
    )

    # Print response
    print("Document Schema Deleted:",response)

# [END contentwarehouse_delete_document_schema]
