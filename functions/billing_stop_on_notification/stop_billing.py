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
# WARNING: The following action, if not in simulation mode, will disable billing
# for the project, potentially stopping all services and causing outages.
# Ensure thorough testing and understanding before enabling live deactivation.

import base64
import json
import os
import urllib.request

from cloudevents.http.event import CloudEvent
import functions_framework

from google.api_core import exceptions
from google.cloud import billing_v1
from google.cloud import logging

billing_client = billing_v1.CloudBillingClient()


def get_project_id() -> str:
    """Retrieves the Google Cloud Project ID.

    This function first attempts to get the project ID from the
    `GOOGLE_CLOUD_PROJECT` environment variable. If the environment
    variable is not set or is None, it then attempts to retrieve the
    project ID from the Google Cloud metadata server.

    Returns:
        str: The Google Cloud Project ID.

    Raises:
        ValueError: If the project ID cannot be determined either from
                    the environment variable or the metadata server.
    """

    # Read the environment variable, usually set manually
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id is not None:
        return project_id

    # Otherwise, get the `project-id`` from the Metadata server
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()

    if project_id is None:
        raise ValueError("project-id metadata not found.")

    return project_id


@functions_framework.cloud_event
def stop_billing(cloud_event: CloudEvent) -> None:
    # TODO(developer): As stoping billing is a destructive action
    # for your project, change the following constant to False
    # after you validate with a test budget.
    SIMULATE_DEACTIVATION = True

    PROJECT_ID = get_project_id()
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

    print(f"Disabling billing for project '{PROJECT_NAME}'...")

    is_billing_enabled = _is_billing_enabled(PROJECT_NAME)

    if is_billing_enabled:
        _disable_billing_for_project(
            PROJECT_NAME,
            SIMULATE_DEACTIVATION
        )
    else:
        print("Billing is already disabled.")


def _is_billing_enabled(project_name: str) -> bool:
    """Determine whether billing is enabled for a project.

    Args:
        project_name: Name of project to check if billing is enabled.

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
    project_name: str,
    simulate_deactivation: bool,
) -> None:
    """Disable billing for a project by removing its billing account.

    Args:
        project_name: Name of project to disable billing.
        simulate_deactivation:
            If True, it won't actually disable billing.
            Useful to validate with test budgets.
    """

    # Log this operation in Cloud Logging
    logging_client = logging.Client()
    logger = logging_client.logger(name="disable-billing")

    if simulate_deactivation:
        entry_text = "Billing disabled. (Simulated)"
        print(entry_text)
        logger.log_text(entry_text, severity="CRITICAL")
        return

    # Find more information about `updateBillingInfo` API method here:
    # https://cloud.google.com/billing/docs/reference/rest/v1/projects/updateBillingInfo
    try:
        # To disable billing set the `billing_account_name` field to empty
        project_billing_info = billing_v1.ProjectBillingInfo(
            billing_account_name=""
        )

        response = billing_client.update_project_billing_info(
            name=project_name,
            project_billing_info=project_billing_info
        )

        entry_text = f"Billing disabled: {response}"
        print(entry_text)
        logger.log_text(entry_text, severity="CRITICAL")
    except exceptions.PermissionDenied:
        print("Failed to disable billing, check permissions.")
# [END functions_billing_stop]
