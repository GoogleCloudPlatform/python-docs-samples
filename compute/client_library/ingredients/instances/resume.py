#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
from google.cloud import compute_v1


# <INGREDIENT resume_instance>
def resume_instance(project_id: str, zone: str, instance_name: str) -> None:
    """
    Resume a suspended Google Compute Engine instance (with unencrypted disks).
    Args:
        project_id: project ID or project number of the Cloud project your instance belongs to.
        zone: name of the zone your instance belongs to.
        instance_name: name of the instance you want to resume.
    """
    instance_client = compute_v1.InstancesClient()

    instance = instance_client.get(project=project_id, zone=zone, instance=instance_name)
    if instance.status != compute_v1.Instance.Status.SUSPENDED.name:
        raise RuntimeError(f"Only suspended instances can be resumed. "
                           f"Instance {instance_name} is in {instance.status} state.")

    operation = instance_client.resume(
        project=project_id, zone=zone, instance=instance_name
    )

    wait_for_extended_operation(operation, "instance resumption")
# </INGREDIENT>
