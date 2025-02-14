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

# [START iam_create_key]
from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


def create_key(project_id: str, account: str) -> types.ServiceAccountKey:
    """
    Creates a key for a service account.

    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.CreateServiceAccountKeyRequest()
    request.name = f"projects/{project_id}/serviceAccounts/{account}"

    key = iam_admin_client.create_service_account_key(request=request)

    # The private_key_data field contains the stringified service account key
    # in JSON format. You cannot download it again later.
    # If you want to get the value, you can do it in a following way:
    # import json
    # json_key_data = json.loads(key.private_key_data)
    # key_id = json_key_data["private_key_id"]

    return key
# [END iam_create_key]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccountKeys.create permission (roles/iam.serviceAccountKeyAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    account_name = "test-account-name"

    # Note: If you have different email format, you can just paste it directly
    email = f"{account_name}@{PROJECT_ID}.iam.gserviceaccount.com"

    create_key(PROJECT_ID, email)
