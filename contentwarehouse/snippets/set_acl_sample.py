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


# [START contentwarehouse_set_acl]

from typing import Dict

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# document_id = 'YOUR_DOCUMENT_ID'
# user_id = 'user:YOUR_SERVICE_ACCOUNT_ID' # Format is "user:xxxx@example.com"
# policy = "Policy in JSON format"


def set_acl(
    project_number: str,
    location: str,
    policy: Dict,
    user_id: str,
    document_id: str = ''
) -> None:
    """Sets access control policies on project or document level.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        policy: ACL policy to set, in JSON format 
        user_id: user:YOUR_SERVICE_ACCOUNT_ID.
        document_id: Record id in Document AI Warehouse.
    """
    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # Initialize request argument(s)
    # Set document acl if document id is specified
    # else set acl on project level
    if document_id:
        request = contentwarehouse.SetAclRequest(
            # The full resource name of the document, e.g.:
            # projects/{project_number}/locations/{location}/documents/{document_id}
            resource=client.document_path(project_number, location, document_id),
            request_metadata=contentwarehouse.RequestMetadata(
                user_info=contentwarehouse.UserInfo(id=user_id)
            ),
        )
    else:
        request = contentwarehouse.SetAclRequest(
            # The full resource name of the project, e.g.:
            # projects/{project_number}
            resource=client.common_project_path(project_number),
            project_owner=True,
        )

    request.policy = policy

    # Make the request
    response = client.set_acl(request=request)

    # Handle the response
    print(response)


# [END contentwarehouse_set_acl]
