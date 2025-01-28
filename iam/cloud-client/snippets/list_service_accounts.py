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

# This file contains code samples that demonstrate how to get list of service account.

import os

# [START iam_list_service_accounts]
from typing import List

from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types


def list_service_accounts(project_id: str) -> List[iam_admin_v1.ServiceAccount]:
    """Get list of project service accounts.

    project_id: ID or number of the Google Cloud project you want to use.

    returns a list of iam_admin_v1.ServiceAccount
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.ListServiceAccountsRequest()
    request.name = f"projects/{project_id}"

    accounts = iam_admin_client.list_service_accounts(request=request)
    return accounts.accounts
# [END iam_list_service_accounts]


def get_service_account(project_id: str, account: str) -> iam_admin_v1.ServiceAccount:
    """Get certain service account.

    Args:
        project_id: ID or number of the Google Cloud project you want to use.
        account_id: ID or email which will be unique identifier
        of the service account.

    Returns: iam_admin_v1.ServiceAccount
    """

    iam_admin_client = iam_admin_v1.IAMClient()
    request = types.GetServiceAccountRequest()
    request.name = f"projects/{project_id}/serviceAccounts/{account}"

    account = iam_admin_client.get_service_account(request=request)
    return account


if __name__ == "__main__":
    # To run the sample you would need
    # iam.serviceAccounts.list permission (roles/iam.serviceAccountViewer))

    # Your Google Cloud project ID.
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")

    list_service_accounts(PROJECT_ID)

    get_service_account(PROJECT_ID, "account_id")
