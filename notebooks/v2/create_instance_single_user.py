# Copyright 2026 Google LLC
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

# [START notebooks_v2_create_instance_single_user]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_single_user(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-single-user-instance",
    instance_owner: str = "example-user@example.com",
    service_account_email: str = "example-sa@example-project-id.iam.gserviceaccount.com",
) -> None:
    """Creates a single-user Workbench instance with a custom service account.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        instance_owner: The email address of the single permitted user.
        service_account_email: The email address of the service account to
            attach to the instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    service_account = notebooks_v2.ServiceAccount(email=service_account_email)
    gce_setup = notebooks_v2.GceSetup(
        machine_type="e2-standard-4",
        service_accounts=[service_account],
    )
    instance = notebooks_v2.Instance(
        gce_setup=gce_setup,
        instance_owners=[instance_owner],
    )
    request = notebooks_v2.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        # The operation completes once the instance is accepted, before the
        # VM finishes provisioning, so the state is usually PROVISIONING here.
        response = operation.result()
        print(f"Resource ID: {response.name}")
        print(f"Creator: {response.creator}")
        print(f"State: {response.state.name}")
        print(
            "The instance is still starting up; call get_instance until the "
            "state is ACTIVE before connecting to JupyterLab."
        )
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_single_user]
