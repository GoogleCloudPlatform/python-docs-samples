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


# [START contentwarehouse_create_document_schema]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'


def sample_create_document_schema(
    project_number: str,
    location: str
) -> None:
    """Creates document schema.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
    """
    # Create a Schema Service client.
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    property_definition = contentwarehouse.PropertyDefinition(
        name="stock_symbol",  # Must be unique within a document schema (case insensitive)
        display_name="Searchable text",
        is_searchable=True,
        text_type_options=contentwarehouse.TextTypeOptions(),
    )
    # Initialize request argument(s)
    document_schema = contentwarehouse.DocumentSchema(
        display_name="My Test Schema",
        property_definitions=[property_definition],
    )

    request = contentwarehouse.CreateDocumentSchemaRequest(
        # The full resource name of the location, e.g.:
        # projects/{project_number}/locations/{location}/
        parent=document_schema_client.common_location_path(
        project_number,
        location),
        document_schema=document_schema,
    )

    # Make the request
    response = document_schema_client.create_document_schema(
        request=request
    )

    # Print response
    print("Document Schema Created:",response)


# [END contentwarehouse_create_document_schema]
