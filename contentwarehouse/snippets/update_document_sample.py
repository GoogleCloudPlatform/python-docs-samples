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

from google.cloud import contentwarehouse


def sample_update_document(
    document_name: str, document: contentwarehouse.Document, user_id: str
) -> contentwarehouse.CreateDocumentResponse:
    """Updates a document.

    Args:
        document_name: The resource name of the document.
                    Format: 'projects/{project_number}/
                    locations/{location}/documents/{document_id}'.
        document: Document AI Warehouse Document object..
        user_id: user_id: user:YOUR_SERVICE_ACCOUNT_ID or user:USER_EMAIL.
    Returns:
        Response object.
    """
    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # Update document fields
    # For fields which can be updated, refer
    # https://cloud.google.com/python/docs/reference/contentwarehouse/
    # latest/google.cloud.contentwarehouse_v1.types.Document
    document.display_name = "Updated Order Invoice"

    request_metadata = contentwarehouse.RequestMetadata(
        user_info=contentwarehouse.UserInfo(id=user_id)
    )

    request = contentwarehouse.UpdateDocumentRequest(
        name=document_name, document=document, request_metadata=request_metadata
    )

    # Make the request
    response = client.update_document(request=request)

    return response


# [END contentwarehouse_update_document]
