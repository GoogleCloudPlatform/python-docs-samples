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

from googleapiclient import discovery


def get_project_id() -> str:
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()

    if project_id is None:
        raise ValueError("PROJECT_ID not found.")

    return project_id


@functions_framework.cloud_event
def stop_billing(cloud_event: CloudEvent) -> None:
    PROJECT_ID = get_project_id()
    PROJECT_NAME = f"projects/{PROJECT_ID}"

    pubsub_data = base64.b64decode(
        cloud_event.data["message"]["data"]
    ).decode("utf-8")
    pubsub_json = json.loads(pubsub_data)

    cost_amount = pubsub_json["costAmount"]
    budget_amount = pubsub_json["budgetAmount"]
    print(f"Cost: {cost_amount} Budget: {budget_amount}")

    if cost_amount <= budget_amount:
        print("No action required. Current cost is within budget.")
        return

    # Construct a Resource for interacting with the billing API
    billing = discovery.build(
        "cloudbilling",
        "v1",
        cache_discovery=False,
    )

    # Get the resource containing the projects
    projects = billing.projects()

    is_billing_enabled = _is_billing_enabled(PROJECT_NAME, projects)

    # Disable billing if required
    if is_billing_enabled:
        _disable_billing_for_project(PROJECT_NAME, projects)
    else:
        print("Billing is already disabled.")


def _is_billing_enabled(
    project_name: str, projects: discovery.Resource
) -> bool:
    """Determine whether billing is enabled for a project.

    Args:
        project_name: Name of project to check if billing is enabled.
        projects: Resource for interacting with the Billing API.

    Returns:
        Whether project has billing enabled or not.
    """
    try:
        print(f"Getting billing info for project: {project_name}")
        res = projects.getBillingInfo(name=project_name).execute()

        return res["billingEnabled"]
    except KeyError:
        # If `billingEnabled` isn't part of the billingInfo,
        # billing is not enabled
        return False
    except Exception:
        print(
            "Unable to determine if billing is enabled on specified project, "
            "assuming billing is enabled"
        )
        return True


def _disable_billing_for_project(
    project_name: str, projects: discovery.Resource
) -> None:
    """Disable billing for a project by removing its billing account.

    Args:
        project_name: Name of project to disable billing.
        projects: Resource for interacting with the Billing API.
    """

    # Find more information about `updateBillingInfo` method here:
    # https://cloud.google.com/billing/docs/reference/rest/v1/projects/updateBillingInfo

    # To disable billing set the `billingAccountName` field to empty
    body = {"billingAccountName": ""}

    try:
        print(f"Disabling billing for project: {project_name}")
        res = projects.updateBillingInfo(name=project_name, body=body).execute()
        print(f"Billing disabled: {json.dumps(res)}")
    except Exception:
        print("Failed to disable billing, check permissions.")
# [END functions_billing_stop]
