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


# [START contentwarehouse_quickstart]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# user_id = "user:xxxx@example.com" # Format is "user:xxxx@example.com"


def quickstart(project_number: str, location: str, user_id: str) -> None:
    # Create a Schema Service client
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = document_schema_client.common_location_path(
        project=project_number, location=location
    )

    # Define Schema Property of Text Type
    property_definition = contentwarehouse.PropertyDefinition(
        name="stock_symbol",  # Must be unique within a document schema (case insensitive)
        display_name="Searchable text",
        is_searchable=True,
        text_type_options=contentwarehouse.TextTypeOptions(),
    )

    # Define Document Schema Request
    create_document_schema_request = contentwarehouse.CreateDocumentSchemaRequest(
        parent=parent,
        document_schema=contentwarehouse.DocumentSchema(
            display_name="My Test Schema",
            property_definitions=[property_definition],
        ),
    )

    # Create a Document schema
    document_schema = document_schema_client.create_document_schema(
        request=create_document_schema_request
    )

    # Create a Document Service client
    document_client = contentwarehouse.DocumentServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = document_client.common_location_path(
        project=project_number, location=location
    )

    # Define Document Property Value
    document_property = contentwarehouse.Property(
        name=document_schema.property_definitions[0].name,
        text_values=contentwarehouse.TextArray(values=["GOOG"]),
    )

    # Define Document
    document = contentwarehouse.Document(
        display_name="My Test Document",
        document_schema_name=document_schema.name,
        plain_text="This is a sample of a document's text.",
        properties=[document_property],
    )

    # Define Request
    create_document_request = contentwarehouse.CreateDocumentRequest(
        parent=parent,
        document=document,
        request_metadata=contentwarehouse.RequestMetadata(
            user_info=contentwarehouse.UserInfo(id=user_id)
        ),
    )

    # Create a Document for the given schema
    response = document_client.create_document(request=create_document_request)

    # Read the output
    print(f"Rule Engine Output: {response.rule_engine_output}")
    print(f"Document Created: {response.document}")


# [END contentwarehouse_quickstart]
