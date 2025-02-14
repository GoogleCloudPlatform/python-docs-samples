# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

# [START iam_rename_service_account]
from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


def rename_service_account(
    project_id: str, account: str, new_name: str
) -> types.ServiceAccount:
    """Renames service account display name.

    project_id: ID or number of the Google Cloud project you want to use.
    account: ID or email which is unique identifier of the service account.
    new_name: New display name of the service account.
    """

    iam_admin_client = iam_admin_v1.IAMClient()

    get_request = types.GetServiceAccountRequest()
    get_request.name = f"projects/{project_id}/serviceAccounts/{account}"
    service_account = iam_admin_client.get_service_account(request=get_request)

    service_account.display_name = new_name

    request = types.PatchServiceAccountRequest()
    request.service_account = service_account
    # You can patch only the `display_name` and `description` fields.
    # You must use the `update_mask` field to specify which of these fields
    # you want to patch.
    # To successfully set update mask you need to transform
    # snake_case field to camelCase.
    # e.g. `display_name` will become `displayName`
    request.update_mask = "displayName"

    updated_account = iam_admin_client.patch_service_account(request=request)
    return updated_account
# [END iam_rename_service_account]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.update permission (roles/iam.serviceAccountAdmin)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    account_name = "test-service-account"
    account_id = f"{account_name}@{PROJECT_ID}.iam.gserviceaccount.com"
    new_name = "New Name"

    rename_service_account(PROJECT_ID, account_id, new_name)
