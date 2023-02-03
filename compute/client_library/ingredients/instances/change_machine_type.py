#  Copyright 2023 Google LLC
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

from typing import NoReturn

from google.cloud import compute_v1


# <INGREDIENT change_machine_type>
def change_machine_type(project_id: str, zone: str, instance_name: str, new_machine_type: str) -> NoReturn:
    """
    Changes the machine type of VM. The VM needs to be in the 'TERMINATED' state for this operation to be successful.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone your instance belongs to.
        instance_name: name of the VM you want to modify.
        new_machine_type: the new machine type you want to use for the VM.
            For example: `e2-standard-8`, `e2-custom-4-2048` or `m1-ultramem-40`
            More about machine types: https://cloud.google.com/compute/docs/machine-resource
    """
    client = compute_v1.InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)

    if instance.status != compute_v1.Instance.Status.TERMINATED.name:
        raise RuntimeError(f"Only machines in TERMINATED state can have their machine type changed. "
                           f"{instance.name} is in {instance.status}({instance.status_message}) state.")

    machine_type = compute_v1.InstancesSetMachineTypeRequest()
    machine_type.machine_type = f"projects/{project_id}/zones/{zone}/machineTypes/{new_machine_type}"
    operation = client.set_machine_type(
        project=project_id,
        zone=zone,
        instance=instance_name,
        instances_set_machine_type_request_resource=machine_type,
    )

    wait_for_extended_operation(operation, "changing machine type")

    return
# </INGREDIENT>
