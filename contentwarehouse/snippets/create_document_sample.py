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

from google.cloud import contentwarehouse

def sample_create_document(
    project_number: str,
    location: str,
    raw_doc_path: str,
    mime_type: str,
    document_schema_id: str,
    user_id: str,
    reference_id: str = ""
):
    """Creates a document.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        raw_doc_path: Raw document file in Cloud Storage path. 
        mime_type: Document format eg. PDF/DOCX etc.
        document_schema_id: Unique identifier for document schema
        user_id: user:YOUR_SERVICE_ACCOUNT_ID or user:USER_EMAIL.
        reference_id: Identifier, must be unique per project and location.
    Returns:
        Response object.
    """
    # Create a Document Service client
    client = contentwarehouse.DocumentServiceClient()

    parent = client.common_location_path(
        project=project_number, location=location
    )

    # Initialize request argument(s)
    document = contentwarehouse.Document()
    mimetype = {"application/pdf": document.raw_document_file_type.RAW_DOCUMENT_FILE_TYPE_PDF}
    document.plain_text = "Sample Order Invoice Document"
    document.raw_document_path = raw_doc_path
    document.display_name = "Order Invoice1"
    document.raw_document_file_type = mimetype[mime_type]
    document.document_schema_name = f"{parent}/documentSchemas/{document_schema_id}"
    document.reference_id = reference_id

    request_metadata = contentwarehouse.RequestMetadata(
        user_info=contentwarehouse.UserInfo(id=user_id)
    )

    request = contentwarehouse.CreateDocumentRequest(
        parent=parent,
        request_metadata=request_metadata,
        document=document,
    )

    # Make the request
    response = client.create_document(request=request)

    return response


# [END contentwarehouse_create_document]
