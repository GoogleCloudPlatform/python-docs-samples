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


# [START contentwarehouse_fetch_acl]

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# document_id = 'YOUR_DOCUMENT_ID'
# user_id = 'user:YOUR_SERVICE_ACCOUNT' # Format is "user:xxxx@example.com"


def fetch_acl(
    project_number: str,
    location: str,
    user_id: str,
    document_id: str = ''
) -> None:
    """Function to fetch access control policies
    on project or document level.

    Args:
        project_number: GCP project number.
        location: GCP project location.
        user_id: Service account.
        document_id: Document id.
    """
    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # Initialize request argument(s)
    # Fetch document acl if document id is specified
    # else fetch acl on project level
    if document_id:
        # The full resource name of the document, e.g.:
        # projects/{project_number}/locations/{location}/documents/{document_id}
        resource = client.document_path(project_number, location, document_id)
    else:
        # The full resource name of the project, e.g.:
        # projects/{project_number}
        resource = client.common_project_path(project_number)

    # Define request
    request = contentwarehouse.FetchAclRequest(
        resource=resource,
        request_metadata=contentwarehouse.RequestMetadata(
            user_info=contentwarehouse.UserInfo(id=user_id)
        )
    )

    response = client.fetch_acl(request)
    print(response)


# [END contentwarehouse_fetch_acl]
