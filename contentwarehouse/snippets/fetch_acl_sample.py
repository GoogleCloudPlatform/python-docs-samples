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
# user_id = 'YOUR_SERVICE_ACCOUNT' # Format is "user:xxxx@example.com"


def fetch_acl(
    project_number: str,
    location: str,
    user_id: str,
    document_id: str = ''
) -> None:

    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = client.common_location_path(
    project=project_number, location=location
    )

    # Define request
    request = contentwarehouse.FetchAclRequest()

    # Initialize request argument(s)
    # Fetch document acl is document id is specified
    # else fetch acl on project level
    if len(document_id)!=0:
        request.resource = f"{parent}/documents/{document_id}"
    else:
        request.resource = f"projects/{project_number}"

    request.request_metadata.user_info.id = user_id
    print(client.fetch_acl(request))


# [END contentwarehouse_fetch_acl]
