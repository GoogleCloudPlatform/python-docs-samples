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


# [START contentwarehouse_create_folder_link_document]

from google.cloud import contentwarehouse
import sys
#TODO(developer): Uncomment these variables before running the sample.
# project_number = "YOUR_PROJECT_NUMBER"
# location = "us" # Format is 'us' or 'eu'

def create_folder(project_number: str, location: str) -> contentwarehouse.Document:
    
    # Create a Schema Service client
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = document_schema_client.common_location_path(
        project=project_number, location=location
    )

    # Define Folder Schema Request
    create_folder_schema_request = contentwarehouse.CreateDocumentSchemaRequest(
        parent=parent,
        document_schema=contentwarehouse.DocumentSchema(
            display_name="Test Folder Schema ",
            document_is_folder = True,
        ),
    )

    # Create a Folder Schema
    folder_schema = document_schema_client.create_document_schema(
        request=create_folder_schema_request
    )

    # Create a Document(Folder) Service client
    folder_client = contentwarehouse.DocumentServiceClient()

    # Define Folder
    folder = contentwarehouse.Document(
        display_name="My Test Folder",
        document_schema_name=folder_schema.name,
    )

    # Define Request to create Folder
    create_folder_request = contentwarehouse.CreateDocumentRequest(
        parent=parent, document=folder, request_metadata=contentwarehouse.RequestMetadata(user_info=contentwarehouse.UserInfo(id="user:valentinhuerta@google.com"))
    )

    # Create a Folder for the given schema
    folder_response = folder_client.create_document(request=create_folder_request)

    # Read the output
    print(f"Rule Engine Output: {folder_response.rule_engine_output}")
    print(f"Folder Created: {folder_response.document}")

    return folder_response

def create_document(project_number: str, location: str) -> contentwarehouse.Document:

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
        parent=parent, document=document, request_metadata=contentwarehouse.RequestMetadata(user_info=contentwarehouse.UserInfo(id="user:valentinhuerta@google.com"))
    )

    # Create a Document for the given schema
    document_response = document_client.create_document(request=create_document_request)

    # Read the output
    print(f"Rule Engine Output: {document_response.rule_engine_output}")
    print(f"Document Created: {document_response.document}")

    return document_response


def create_folder_link_document(project_number: str, location: str) -> None:

    #Function call to create a folder
    folder = create_folder(project_number,location)

    #Function call to create a Document
    document = create_document(project_number,location)

    # Create a Link Service client
    link_client = contentwarehouse.DocumentLinkServiceClient()

    # Initialize request argument(s)
    link = contentwarehouse.DocumentLink(
        source_document_reference = contentwarehouse.DocumentReference(
            document_name = folder.document.name,
        ),
        target_document_reference = contentwarehouse.DocumentReference(
            document_name = document.document.name,
        ),
    )
    
    # Initialize document link request
    create_document_link_request = contentwarehouse.CreateDocumentLinkRequest(
        parent=folder.document.name,
        document_link=link,
        request_metadata=contentwarehouse.RequestMetadata(user_info=contentwarehouse.UserInfo(id="user:valentinhuerta@google.com"))
    )

    # Make the Document Link request
    create_link_response = link_client.create_document_link(request=create_document_link_request)

    print(f"Link Created: {create_link_response}")
    
    # Initialize list linked targets request
    linked_targets_request = contentwarehouse.ListLinkedTargetsRequest(
        parent=folder.document.name,
        request_metadata=contentwarehouse.RequestMetadata(user_info=contentwarehouse.UserInfo(id="user:valentinhuerta@google.com"))
    )

    # Make the request
    linked_targets_response = link_client.list_linked_targets(request=linked_targets_request)

    print(f"Validate Link Created: {linked_targets_response}")
# [END contentwarehouse_create_folder_link_document]