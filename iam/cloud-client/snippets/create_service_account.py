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

# This file contains code samples that demonstrate
# how to create a service account.

import os

# [START iam_create_service_account]
from typing import Optional

from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


def create_service_account(
    project_id: str, account_id: str, display_name: Optional[str] = None
) -> types.ServiceAccount:
    """Creates a service account.

    project_id: ID or number of the Google Cloud project you want to use.
    account_id: ID which will be unique identifier of the service account
    display_name (optional): human-readable name, which will be assigned
        to the service account

    return: ServiceAccount
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.CreateServiceAccountRequest()

    request.account_id = account_id
    request.name = f"projects/{project_id}"

    service_account = types.ServiceAccount()
    service_account.display_name = display_name
    request.service_account = service_account

    account = iam_admin_client.create_service_account(request=request)

    print(f"Created a service account: {account.email}")
    return account
# [END iam_create_service_account]


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.create permission (roles/iam.serviceAccountCreator)

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    # Existing service account name within the project specified above.
    ACCOUNT_ID = os.getenv("ACCOUNT_ID", "test-service-account")
    DISPLAY_NAME = ACCOUNT_ID

    create_service_account(PROJECT_ID, ACCOUNT_ID, DISPLAY_NAME)
