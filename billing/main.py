# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json

import google.auth
from google.cloud import billing


PROJECT_ID = google.auth.default()[1]
cloud_billing_client = billing.CloudBillingClient()


def stop_billing(data: dict, context):
    pubsub_data = base64.b64decode(data["data"]).decode("utf-8")
    pubsub_json = json.loads(pubsub_data)
    cost_amount = pubsub_json["costAmount"]
    budget_amount = pubsub_json["budgetAmount"]
    if cost_amount <= budget_amount:
        print(f"No action necessary. (Current cost: {cost_amount})")
        return

    project_name = cloud_billing_client.common_project_path(PROJECT_ID)
    billing_enabled = _is_billing_enabled(project_name)

    if billing_enabled:
        _disable_billing_for_project(project_name)
    else:
        print("Billing already disabled")


def _is_billing_enabled(project_name: str) -> bool:
    """Determine whether billing is enabled for a project

    Args:
        project_name (str): Name of project to check if billing is enabled

    Returns:
        bool: Whether project has billing enabled or not
    """
    request = billing.GetProjectBillingInfoRequest(name=project_name)
    project_billing_info = cloud_billing_client.get_project_billing_info(request)

    return project_billing_info.billing_enabled


def _disable_billing_for_project(project_name: str) -> None:
    """Disable billing for a project by removing its billing account

    Args:
        project_name (str): Name of project disable billing on
    """
    request = billing.UpdateProjectBillingInfoRequest(
        name=project_name,
        project_billing_info=billing.ProjectBillingInfo(
            billing_account_name=""  # Disable billing
        ),
    )
    project_biling_info = cloud_billing_client.update_project_billing_info(request)
    print(f"Billing disabled: {project_biling_info}")
