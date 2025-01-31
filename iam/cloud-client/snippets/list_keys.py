# Copyright 2024 Google LLC
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

# This file contains code samples that demonstrate how to get create IAM key for service account.

import os

# [START iam_list_keys]
from typing import List

from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


def list_keys(project_id: str, account: str) -> List[iam_admin_v1.ServiceAccountKey]:
    """Creates a key for a service account.

    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.ListServiceAccountKeysRequest()
    request.name = f"projects/{project_id}/serviceAccounts/{account}"

    response = iam_admin_client.list_service_account_keys(request=request)
    return response.keys
# [END iam_list_keys]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccountKeys.list permission (roles/iam.serviceAccountKeyAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    account_name = "test-account-name"
    # Note: If you have different email format, you can just paste it directly
    email = f"{account_name}@{PROJECT_ID}.iam.gserviceaccount.com"

    list_keys(PROJECT_ID, email)
