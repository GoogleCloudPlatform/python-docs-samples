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
# schema_display_name = 'YOUR_SCHEMA_DISPLAY_NAME'
# property_name = 'YOUR_PROPERTY_NAME' # Must be unique within a document schema (case insensitive)
# property_display_name = 'YOUR_PROPERTY_DISPLAY_NAME'
# property_is_searchable = True
# document_display_name = 'YOUR_DOCUMENT_DISPLAY_NAME'
# document_plain_text = 'YOUR_DOCUMENT_TEXT'
# document_property_value = 'YOUR_PROPERTY_VALUE'


def quickstart(
    project_number: str,
    location: str,
    schema_display_name: str,
    property_name: str,
    property_display_name: str,
    property_is_searchable: bool,
    document_display_name: str,
    document_plain_text: str,
    document_property_value: str,
) -> None:

    # Create a Document schema
    document_schema = create_document_schema(
        project_number,
        location,
        schema_display_name,
        property_name,
        property_display_name,
        property_is_searchable,
    )

    # Create a Document for the given schema
    create_document_response = create_document(
        project_number,
        location,
        document_schema,
        document_display_name,
        document_plain_text,
        document_property_value,
    )

    # Read the output
    print(f"Rule Engine Output: {create_document_response.rule_engine_output}")
    print(f"Document Created: {create_document_response.document}")


def create_document_schema(
    project_number: str,
    location: str,
    schema_display_name: str,
    property_name: str,
    property_display_name: str,
    property_is_searchable: bool,
) -> contentwarehouse.DocumentSchema:
    # Create a client
    client = contentwarehouse.DocumentSchemaServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = client.common_location_path(project=project_number, location=location)

    # Define Schema Property of Text Type
    property_definition = contentwarehouse.PropertyDefinition(
        name=property_name,
        display_name=property_display_name,
        is_searchable=property_is_searchable,
        text_type_options=contentwarehouse.TextTypeOptions(),
    )

    # Define Document Schema
    document_schema = contentwarehouse.DocumentSchema(
        display_name=schema_display_name, property_definitions=[property_definition]
    )

    # Define Request
    request = contentwarehouse.CreateDocumentSchemaRequest(
        parent=parent,
        document_schema=document_schema,
    )

    # Make the request
    response = client.create_document_schema(request=request)

    return response


def create_document(
    project_number: str,
    location: str,
    document_schema: contentwarehouse.DocumentSchema,
    display_name: str,
    plain_text: str,
    property_value: str,
) -> contentwarehouse.CreateDocumentResponse:
    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = client.common_location_path(project=project_number, location=location)

    # Define Document Property Value
    document_property = contentwarehouse.Property(
        name=document_schema.property_definitions[0].name,
        text_values=contentwarehouse.TextArray(values=[property_value]),
    )

    # Define Document
    document = contentwarehouse.Document(
        display_name=display_name,
        document_schema_name=document_schema.name,
        plain_text=plain_text,
        properties=[document_property],
    )

    # Define Request
    request = contentwarehouse.CreateDocumentRequest(parent=parent, document=document)

    # Make the request
    response = client.create_document(request=request)

    return response


# [END contentwarehouse_quickstart]
