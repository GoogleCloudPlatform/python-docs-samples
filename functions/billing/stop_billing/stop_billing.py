# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_billing_stop]
import base64
import json
import urllib.request

from cloudevents.http.event import CloudEvent
import functions_framework

from google.api_core import exceptions
from google.cloud import billing_v1


def get_project_id_from_metadata() -> str:
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()

    if project_id is None:
        raise ValueError("PROJECT_ID not found.")

    return project_id


@functions_framework.cloud_event
def stop_billing(cloud_event: CloudEvent) -> None:
    PROJECT_ID = get_project_id_from_metadata()
    PROJECT_NAME = f"projects/{PROJECT_ID}"

    event_data = base64.b64decode(
        cloud_event.data["message"]["data"]
    ).decode("utf-8")
    event_dict = json.loads(event_data)

    cost_amount = event_dict["costAmount"]
    budget_amount = event_dict["budgetAmount"]
    print(f"Cost: {cost_amount} Budget: {budget_amount}")

    if cost_amount <= budget_amount:
        print("No action required. Current cost is within budget.")
        return

    # Create a Billing client.
    billing_client = billing_v1.CloudBillingClient()

    is_billing_enabled = _is_billing_enabled(PROJECT_NAME, billing_client)

    # Disable billing if required
    if is_billing_enabled:
        _disable_billing_for_project(PROJECT_NAME, billing_client)
    else:
        print("Billing is already disabled.")


def _is_billing_enabled(
    project_name: str, billing_client: billing_v1.CloudBillingClient
) -> bool:
    """Determine whether billing is enabled for a project.

    Args:
        project_name: Name of project to check if billing is enabled.
        projects: Resource for interacting with the Billing API.

    Returns:
        Whether project has billing enabled or not.
    """
    try:
        print(f"Getting billing info for project '{project_name}'...")
        response = billing_client.get_project_billing_info(name=project_name)

        return response.billing_enabled
    except Exception as e:
        print(f'Error getting billing info: {e}')
        print(
            "Unable to determine if billing is enabled on specified project, "
            "assuming billing is enabled."
        )

        return True


def _disable_billing_for_project(
    project_name: str, billing_client: billing_v1.CloudBillingClient
) -> None:
    """Disable billing for a project by removing its billing account.

    Args:
        project_name: Name of project to disable billing.
        projects: Resource for interacting with the Billing API.
    """

    print(f"Disabling billing for project '{project_name}'...")

    # To disable billing set the `billing_account_name` field to empty
    # LINT: Commented out to pass linter
    # project_billing_info = billing_v1.ProjectBillingInfo(
    #     billing_account_name=""
    # )

    # Find more information about `updateBillingInfo` API method here:
    # https://cloud.google.com/billing/docs/reference/rest/v1/projects/updateBillingInfo
    try:
        # DEBUG: Simulate disabling billing
        print("Billing disabled. (Simulated)")

        # response = billing_client.update_project_billing_info(
        #     name=project_name,
        #     project_billing_info=project_billing_info
        # )
        # print(f"Billing disabled: {response}")
    except exceptions.PermissionDenied:
        print("Failed to disable billing, check permissions.")
# [END functions_billing_stop]
