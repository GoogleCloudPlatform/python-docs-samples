#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
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

# [START servicedirectory_quickstart]
from google.cloud import servicedirectory_v1
from google.cloud.servicedirectory_v1.services.registration_service.pagers import (
    ListNamespacesPager,
)


def list_namespaces(project_id: str, location: str) -> ListNamespacesPager:
    """Lists all namespaces in the given location.

    Args:
        project_id: The Google Cloud project id.
        location: The location which contains the namespaces to list.

    Returns:
        All namespaces in the given location.
    """

    client = servicedirectory_v1.RegistrationServiceClient()

    response = client.list_namespaces(
        parent=f"projects/{project_id}/locations/{location}"
    )

    print(f"Listed namespaces in {location}.")
    for namespace in response:
        print(f"Namespace: {namespace.name}")

    return response


# [END servicedirectory_quickstart]
