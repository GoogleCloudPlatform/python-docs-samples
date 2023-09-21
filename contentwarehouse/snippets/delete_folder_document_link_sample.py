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


# [START delete_folder_document_link_sample]
import sys
from google.cloud import contentwarehouse
# TODO(developer): Uncomment these variables before running the sample.
# document_folder_link_name = "YOUR_DOCUMENT_LINK_NAME" # The name of the document-link to be deleted Format: projects/{project_number}/locations/{location}/documents/{source_document_id}/documentLinks/{document_link_id}
# document_name = "YOUR_DOCUMENT_NAME" # The name of the document to be deleted Format: projects/{project_number}/locations/{location}/documents/{target_document_id
# user_id = "user:xxxx@example.com" # Format is "user:xxxx@example.com"

def delete_folder_document_link(document_folder_link_name: str, document_name: str, user_id: str) -> None:

    # Create a Link Service client
    link_client = contentwarehouse.DocumentLinkServiceClient()

    # Initialize delete document linked request
    delete_link_request = contentwarehouse.DeleteDocumentLinkRequest(
        name=document_folder_link_name,
        request_metadata=contentwarehouse.RequestMetadata(
            user_info=contentwarehouse.UserInfo(id=user_id))
    )

    # Make the delete request
    link_client.delete_document_link(request=delete_link_request)

     # Initialize list linked targets request to verify deletion
    linked_targets_request = contentwarehouse.ListLinkedTargetsRequest(
        parent=document_name,
        request_metadata=contentwarehouse.RequestMetadata(
            user_info=contentwarehouse.UserInfo(id=user_id))
    )

    # Make the request
    linked_targets_response = link_client.list_linked_targets(request=linked_targets_request)

    #linked_targets_response returns False if link does not exist
    if bool(linked_targets_response) is False:
        print(f"Document Link to Folder Deleted Successfully")
# [END delete_folder_document_link_sample]
