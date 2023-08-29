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


# [START contentwarehouse_update_document]

from google.cloud import contentwarehouse_v1 as contentwarehouse


def sample_update_document(
    project_number: str,
    location: str,
    mime_type: str,
    document_schema_id: str,
    document_id: str,
    user_id: str,
) -> contentwarehouse.types.CreateDocumentResponse:
    """Updates a document.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        mime_type: Document format eg. PDF/DOCX etc.
        document_schema_id: Unique identifier for document schema.
        document_id: Unique identifier for document.
        user_id: user:YOUR_SERVICE_ACCOUNT_ID or user:USER_EMAIL.
    Returns:
        Response object.
    """
    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    parent = client.common_location_path(project=project_number, location=location)

    # Initialize request argument(s)
    document = contentwarehouse.Document()
    mimetype = {
        "application/pdf": document.raw_document_file_type.RAW_DOCUMENT_FILE_TYPE_PDF
    }
    document.plain_text = "Updated Sample Invoice Document"
    document.display_name = "Order Invoice"
    document.raw_document_file_type = mimetype[mime_type]
    document.document_schema_name = f"{parent}/documentSchemas/{document_schema_id}"

    request_metadata = contentwarehouse.RequestMetadata(
        user_info=contentwarehouse.UserInfo(id=user_id)
    )

    request = contentwarehouse.UpdateDocumentRequest(
        name=f"{parent}/documents/{document_id}",
        request_metadata=request_metadata,
        document=document,
    )

    # Make the request
    response = client.update_document(request=request)

    return response


# [END contentwarehouse_update_document]
