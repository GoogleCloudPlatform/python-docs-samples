#  Copyright 2021 Google LLC
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
# [START compute_custom_machine_type_create ]
from collections import namedtuple
from enum import Enum, unique
import sys
import time
from typing import Union

from google.cloud import compute_v1


# [END compute_custom_machine_type_create ]


# [START compute_custom_machine_type_helper_class ]
def gb_to_mb(value: int) -> int:
    return value << 10


class CustomMachineType:
    """
    Allows to create custom machine types to be used with the VM instances.
    """

    @unique
    class CPUSeries(Enum):
        N1 = "custom"
        N2 = "n2-custom"
        N2D = "n2d-custom"
        E2 = "e2-custom"
        E2_MICRO = "e2-custom-micro"
        E2_SMALL = "e2-custom-small"
        E2_MEDIUM = "e2-custom-medium"

    TypeLimits = namedtuple(
        "TypeLimits",
        [
            "allowed_cores",
            "min_mem_per_core",
            "max_mem_per_core",
            "allow_extra_memory",
            "extra_memory_limit",
        ],
    )

    LIMITS = {
        CPUSeries.E2: TypeLimits(frozenset(range(2, 33, 2)), 512, 8192, False, 0),
        CPUSeries.E2_MICRO: TypeLimits(frozenset(), 1024, 2048, False, 0),
        CPUSeries.E2_SMALL: TypeLimits(frozenset(), 2048, 4096, False, 0),
        CPUSeries.E2_MEDIUM: TypeLimits(frozenset(), 4096, 8192, False, 0),
        CPUSeries.N2: TypeLimits(
            frozenset(range(2, 33, 2)).union(set(range(36, 129, 4))),
            512,
            8192,
            True,
            gb_to_mb(624),
        ),
        CPUSeries.N2D: TypeLimits(
            frozenset({2, 4, 8, 16, 32, 48, 64, 80, 96}), 512, 8192, True, gb_to_mb(768)
        ),
        CPUSeries.N1: TypeLimits(
            frozenset({1}.union(range(2, 97, 2))), 922, 6656, True, gb_to_mb(624)
        ),
    }

    def __init__(
        self, zone: str, cpu_series: CPUSeries, memory_mb: int, core_count: int = 0
    ):
        self.zone = zone
        self.cpu_series = cpu_series
        self.limits = self.LIMITS[self.cpu_series]
        self.core_count = 2 if self.is_shared() else core_count
        self.memory_mb = memory_mb

        self._check()
        self.extra_memory_used = self._check_extra_memory()

    def is_shared(self):
        return self.cpu_series in (
            CustomMachineType.CPUSeries.E2_SMALL,
            CustomMachineType.CPUSeries.E2_MICRO,
            CustomMachineType.CPUSeries.E2_MEDIUM,
        )

    def _check_extra_memory(self) -> bool:
        # Assuming this runs after _check() and the total memory requested is correct
        return self.memory_mb > self.core_count * self.limits.max_mem_per_core

    def _check(self):
        """
        Check whether the requested parameters are allowed. Find more information about limitations of custom machine
        types at: https://cloud.google.com/compute/docs/general-purpose-machines#custom_machine_types
        """
        # Check the number of cores
        if (
            self.limits.allowed_cores
            and self.core_count not in self.limits.allowed_cores
        ):
            raise RuntimeError(
                f"Invalid number of cores requested. Allowed number of cores for {self.cpu_series.name} is: {sorted(self.limits.allowed_cores)}"
            )

        # Memory must be a multiple of 256 MB
        if self.memory_mb % 256 != 0:
            raise RuntimeError("Requested memory must be a multiple of 256 MB.")

        # Check if the requested memory isn't too little
        if self.memory_mb < self.core_count * self.limits.min_mem_per_core:
            raise RuntimeError(
                f"Requested memory is too low. Minimal memory for {self.cpu_series.name} is {self.limits.min_mem_per_core} MB per core."
            )

        # Check if the requested memory isn't too much
        if self.memory_mb > self.core_count * self.limits.max_mem_per_core:
            if self.limits.allow_extra_memory:
                if self.memory_mb > self.limits.extra_memory_limit:
                    raise RuntimeError(
                        f"Requested memory is too large.. Maximum memory allowed for {self.cpu_series.name} is {self.limits.extra_memory_limit} MB."
                    )
            else:
                raise RuntimeError(
                    f"Requested memory is too large.. Maximum memory allowed for {self.cpu_series.name} is {self.limits.max_mem_per_core} MB per core."
                )

    def __str__(self) -> str:
        """
        Return the custom machine type in form of a string acceptable by Compute Engine API.
        """
        if self.cpu_series in {
            self.CPUSeries.E2_SMALL,
            self.CPUSeries.E2_MICRO,
            self.CPUSeries.E2_MEDIUM,
        }:
            return f"zones/{self.zone}/machineTypes/{self.cpu_series.value}-{self.memory_mb}"

        if self.extra_memory_used:
            return f"zones/{self.zone}/machineTypes/{self.cpu_series.value}-{self.core_count}-{self.memory_mb}-ext"

        return f"zones/{self.zone}/machineTypes/{self.cpu_series.value}-{self.core_count}-{self.memory_mb}"

    def short_type_str(self) -> str:
        """
        Return machine type in a format without the zone. For example, n2-custom-0-10240.
        This format is used to create instance templates.
        """
        return str(self).rsplit("/", maxsplit=1)[1]

    @classmethod
    def from_str(cls, machine_type: str):
        """
        Construct a new object from a string. The string needs to be a valid custom machine type like:
         - https://www.googleapis.com/compute/v1/projects/diregapic-mestiv/zones/us-central1-b/machineTypes/e2-custom-4-8192
         - zones/us-central1-b/machineTypes/e2-custom-4-8192
         - e2-custom-4-8192 (in this case, the zone parameter will not be set)
        """
        zone = None
        if machine_type.startswith("http"):
            machine_type = machine_type[machine_type.find("zones/") :]

        if machine_type.startswith("zones/"):
            _, zone, _, machine_type = machine_type.split("/")

        extra_mem = machine_type.endswith("-ext")

        if machine_type.startswith("custom"):
            cpu = cls.CPUSeries.N1
            _, cores, memory = machine_type.rsplit("-", maxsplit=2)
        else:
            if extra_mem:
                cpu_series, _, cores, memory, _ = machine_type.split("-")
            else:
                cpu_series, _, cores, memory = machine_type.split("-")
            if cpu_series == "n2":
                cpu = cls.CPUSeries.N2
            elif cpu_series == "n2d":
                cpu = cls.CPUSeries.N2D
            elif cpu_series == "e2":
                cpu = cls.CPUSeries.E2
                if cores == "micro":
                    cpu = cls.CPUSeries.E2_MICRO
                    cores = 2
                elif cores == "small":
                    cpu = cls.CPUSeries.E2_SMALL
                    cores = 2
                elif cores == "medium":
                    cpu = cls.CPUSeries.E2_MEDIUM
                    cores = 2
            else:
                raise RuntimeError("Unknown CPU series.")

        cores = int(cores)
        memory = int(memory)

        return cls(zone, cpu, memory, cores)


# [END compute_custom_machine_type_helper_class ]


# [START compute_custom_machine_type_create ]
def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    machine_type: Union[str, "CustomMachineType"],
):
    """
    Send an instance creation request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        machine_type: machine type of the VM being created. This value uses the
            following format: "zones/{zone}/machineTypes/{type_name}".
            For example: "zones/europe-west3-c/machineTypes/f1-micro"
            OR
            It can be a CustomMachineType object, describing a custom type
            you want to use.

    Return:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    # Describe the size and source image of the boot disk to attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-10"
    )
    initialize_params.disk_size_gb = 10
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    disk.type_ = compute_v1.AttachedDisk.Type.PERSISTENT.name

    # Use the network interface provided in the network_name argument.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.disks = [disk]
    instance.machine_type = str(machine_type)
    instance.network_interfaces = [network_interface]

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(
        f"Creating the {instance_name} instance of type {instance.machine_type} in {zone}..."
    )
    operation = instance_client.insert_unary(request=request)
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
    if operation.error:
        print("Error during creation:", operation.error, file=sys.stderr)
    if operation.warnings:
        print("Warning during creation:", operation.warnings, file=sys.stderr)
    print(f"Instance {instance_name} created.")
    return instance_client.get(project=project_id, zone=zone, instance=instance.name)


# [END compute_custom_machine_type_create ]


# [START compute_custom_machine_type_create_with_helper ]
def create_custom_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    cpu_series: CustomMachineType.CPUSeries,
    core_count: int,
    memory: int,
) -> compute_v1.Instance:
    """
    Create a new VM instance with a custom machine type.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        cpu_series: the type of CPU you want to use. Select one value from the CustomMachineType.CPUSeries enum.
            For example: CustomMachineType.CPUSeries.N2
        core_count: number of CPU cores you want to use.
        memory: the amount of memory for the VM instance, in megabytes.

    Return:
        Instance object.
    """
    assert cpu_series in (
        CustomMachineType.CPUSeries.E2,
        CustomMachineType.CPUSeries.N1,
        CustomMachineType.CPUSeries.N2,
        CustomMachineType.CPUSeries.N2D,
    )
    custom_type = CustomMachineType(zone, cpu_series, memory, core_count)
    return create_instance(project_id, zone, instance_name, custom_type)


# [END compute_custom_machine_type_create_with_helper ]


# [START compute_custom_machine_type_create_shared_with_helper ]
def create_custom_shared_core_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    cpu_series: CustomMachineType.CPUSeries,
    memory: int,
):
    """
    Create a new VM instance with a custom type using shared CPUs.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        cpu_series: the type of CPU you want to use. Pick one value from the CustomMachineType.CPUSeries enum.
            For example: CustomMachineType.CPUSeries.E2_MICRO
        memory: the amount of memory for the VM instance, in megabytes.

    Return:
        Instance object.
    """
    assert cpu_series in (
        CustomMachineType.CPUSeries.E2_MICRO,
        CustomMachineType.CPUSeries.E2_SMALL,
        CustomMachineType.CPUSeries.E2_MEDIUM,
    )
    custom_type = CustomMachineType(zone, cpu_series, memory)
    return create_instance(project_id, zone, instance_name, custom_type)


# [END compute_custom_machine_type_create_shared_with_helper ]


# [START compute_custom_machine_type_create_without_helper ]
def create_custom_instances_no_helper(
    project_id: str, zone: str, instance_name: str, core_count: int, memory: int
):
    """
    Create new VM instances without using a CustomMachineType helper function.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        core_count: number of CPU cores you want to use.
        memory: the amount of memory for the VM instance, in megabytes.

    Returns:
        List of Instance objects.
    """
    # The core_count and memory values are not validated anywhere and can be rejected by the API.
    instances = [
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n1",
            f"zones/{zone}/machineTypes/custom-{core_count}-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2",
            f"zones/{zone}/machineTypes/n2-custom-{core_count}-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2d",
            f"zones/{zone}/machineTypes/n2d-custom-{core_count}-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_e2",
            f"zones/{zone}/machineTypes/e2-custom-{core_count}-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_e2_micro",
            f"zones/{zone}/machineTypes/e2-custom-micro-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_e2_small",
            f"zones/{zone}/machineTypes/e2-custom-small-{memory}",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_e2_medium",
            f"zones/{zone}/machineTypes/e2-custom-medium-{memory}",
        ),
    ]
    return instances


# [END compute_custom_machine_type_create_without_helper ]


# [START compute_custom_machine_type_extra_mem_no_helper ]
def create_custom_instances_extra_mem_no_helper(
    project_id: str, zone: str, instance_name: str, core_count: int, memory: int
):
    """
    Create new VM instances with extra memory without using a CustomMachineType helper class.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        core_count: number of CPU cores you want to use.
        memory: the amount of memory for the VM instance, in megabytes.

    Returns:
        List of Instance objects.
    """
    # The core_count and memory values are not validated anywhere and can be rejected by the API.
    instances = [
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n1_extra_mem",
            f"zones/{zone}/machineTypes/custom-{core_count}-{memory}-ext",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2_extra_mem",
            f"zones/{zone}/machineTypes/n2-custom-{core_count}-{memory}-ext",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2d_extra_mem",
            f"zones/{zone}/machineTypes/n2d-custom-{core_count}-{memory}-ext",
        ),
    ]
    return instances


# [END compute_custom_machine_type_extra_mem_no_helper ]


# [START compute_custom_machine_type_update_memory ]
def add_extended_memory_to_instance(
    project_id: str, zone: str, instance_name: str, new_memory: int
):
    """
    Modify an existing VM to use extended memory.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        new_memory: the amount of memory for the VM instance, in megabytes.

    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()
    instance = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )

    # Make sure that the machine is turned off
    if instance.status not in (
        instance.Status.TERMINATED.name,
        instance.Status.STOPPED.name,
    ):
        op = instance_client.stop_unary(
            project=project_id, zone=zone, instance=instance_name
        )
        operation_client.wait(project=project_id, zone=zone, operation=op.name)
        while instance.status not in (
            instance.Status.TERMINATED.name,
            instance.Status.STOPPED.name,
        ):
            # Waiting for the instance to be turned off.
            instance = instance_client.get(
                project=project_id, zone=zone, instance=instance_name
            )
            time.sleep(2)

    # Modify the machine definition, remember that extended memory is available only for N1, N2 and N2D CPUs
    start, end = instance.machine_type.rsplit("-", maxsplit=1)
    instance.machine_type = start + f"-{new_memory}-ext"
    # Using CustomMachineType helper
    # cmt = CustomMachineType.from_str(instance.machine_type)
    # cmt.memory_mb = new_memory
    # cmt.extra_memory_used = True
    # instance.machine_type = str(cmt)
    op = instance_client.update_unary(
        project=project_id,
        zone=zone,
        instance=instance_name,
        instance_resource=instance,
    )
    operation_client.wait(project=project_id, zone=zone, operation=op.name)

    return instance_client.get(project=project_id, zone=zone, instance=instance_name)


# [END compute_custom_machine_type_update_memory ]
