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


# [START contentwarehouse_create_document]

from typing import Optional

from google.cloud import contentwarehouse


def sample_create_document(
    project_number: str,
    location: str,
    raw_document_path: str,
    raw_document_file_type: contentwarehouse.RawDocumentFileType,
    document_schema_id: str,
    user_id: str,
    reference_id: Optional[str] = None,
) -> contentwarehouse.CreateDocumentResponse:
    """Creates a document.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        raw_document_path: Raw document file in Cloud Storage path.
        raw_document_file_type: Document file type
                                https://cloud.google.com/python/docs/
                                reference/contentwarehouse/latest/
                                google.cloud.contentwarehouse_v1.types.RawDocumentFileType.
        document_schema_id: Unique identifier for document schema.
        user_id: user:YOUR_SERVICE_ACCOUNT_ID or user:USER_EMAIL.
        reference_id: Identifier, must be unique per project and location.
    Returns:
        Response object.
    """
    # Create a Document Service client
    client = contentwarehouse.DocumentServiceClient()

    # Get document schema name
    document_schema_name = client.document_schema_path(
        project=project_number, location=location, document_schema=document_schema_id
    )

    # Initialize request argument(s)
    document = contentwarehouse.Document(
        raw_document_path=raw_document_path,
        display_name="Order Invoice",
        plain_text="Sample Invoice Document",
        raw_document_file_type=raw_document_file_type,
        document_schema_name=document_schema_name,
        reference_id=reference_id,
    )

    request_metadata = contentwarehouse.RequestMetadata(
        user_info=contentwarehouse.UserInfo(id=user_id)
    )

    parent = client.common_location_path(project=project_number, location=location)

    request = contentwarehouse.CreateDocumentRequest(
        parent=parent,
        request_metadata=request_metadata,
        document=document,
    )

    # Make the request
    response = client.create_document(request=request)

    return response


# [END contentwarehouse_create_document]
