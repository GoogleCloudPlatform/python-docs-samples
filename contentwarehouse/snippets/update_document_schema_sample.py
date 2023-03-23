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


# [START contentwarehouse_update_document_schema]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = "YOUR_PROJECT_NUMBER"
# location = "us" # Format is 'us' or 'eu'
# document_schema_id = "YOUR_SCHEMA_ID"

def update_document_schema(project_number: str, location: str, document_schema_id: str) -> None:

    # Create a Schema Service client
    document_schema_client=contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}
    document_schema_path=document_schema_client.document_schema_path(
        project=project_number, location=location, document_schema=document_schema_id,
    )

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent=document_schema_client.common_location_path(
        project=project_number, location=location
    )

    # Create a Document Service client
    document_client=contentwarehouse.DocumentServiceClient()

    # Define Schema Property of Text Type with updated values
    updated_property_definition=contentwarehouse.PropertyDefinition(
        name="stock_symbol",  # Must be unique within a document schema (case insensitive)
        display_name="Searchable text",
        is_searchable=True,
        is_repeatable=False,
        is_required=True,
        text_type_options=contentwarehouse.TextTypeOptions(),
    )

    # Define Update Document Schema Request
    update_document_schema_request=contentwarehouse.UpdateDocumentSchemaRequest(
        name=document_schema_path,
        document_schema=contentwarehouse.DocumentSchema(
            display_name="My Test Schema",
            property_definitions=[updated_property_definition],
        ),
    )

    # Update Document schema
    updated_document_schema=document_schema_client.update_document_schema(
        request=update_document_schema_request
    )

    # Define Document Property Value for new document
    updated_document_property=contentwarehouse.Property(
        name=updated_document_schema.property_definitions[0].name,
        text_values=contentwarehouse.TextArray(values=["GOOG"]),
    )

    # Define New Document
    new_document=contentwarehouse.Document(
        display_name="My Test Document Updated Schema",
        document_schema_name=updated_document_schema.name,
        plain_text="This is a sample of a document's text.",
        properties=[updated_document_property],
    )

    # Define Request
    create_new_document_request=contentwarehouse.CreateDocumentRequest(
        parent=parent, document=new_document, request_metadata=contentwarehouse.RequestMetadata(user_info=contentwarehouse.UserInfo(id="user:valentinhuerta@google.com"))
    )

    # Create a Document for the given schema
    response=document_client.create_document(request=create_new_document_request)

    # Read the output
    print(f"Rule Engine Output: {response.rule_engine_output}")
    print(f"Document Created: {response.document}")

# [END contentwarehouse_update_document_schema]
