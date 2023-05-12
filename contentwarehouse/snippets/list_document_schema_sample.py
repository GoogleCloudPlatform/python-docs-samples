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


# [START contentwarehouse_get_document_schemas]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'


def sample_list_document_schemas(
    project_number: str,
    location: str
) -> None:
    """Lists document schemas.
    
    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
    """
    # Create a client
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = document_schema_client.common_location_path(
        project=project_number,
        location=location
    )

    # Initialize request argument(s)
    request = contentwarehouse.ListDocumentSchemasRequest(
        parent=parent,
    )

    # Make the request
    page_result = document_schema_client.list_document_schemas(request=request)

    # Print response
    print("Document Schemas:")
    for response in page_result:
        print(response)


# [END contentwarehouse_list_document_schemas]
