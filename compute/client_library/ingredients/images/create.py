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

from __future__ import annotations

import warnings

from google.cloud import compute_v1

# <INGREDIENT create_image>
STOPPED_MACHINE_STATUS = (
    compute_v1.Instance.Status.TERMINATED.name,
    compute_v1.Instance.Status.STOPPED.name
)


def create_image_from_disk(project_id: str, zone: str, source_disk_name: str, image_name: str,
                           storage_location: str | None = None, force_create: bool = False) -> compute_v1.Image:
    """
    Creates a new disk image.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        zone: zone of the disk you copy from.
        source_disk_name: name of the source disk you copy from.
        image_name: name of the image you want to create.
        storage_location: storage location for the image. If the value is undefined,
            function will store the image in the multi-region closest to your image's
            source location.
        force_create: create the image even if the source disk is attached to a
            running instance.

    Returns:
        An Image object.
    """
    image_client = compute_v1.ImagesClient()
    disk_client = compute_v1.DisksClient()
    instance_client = compute_v1.InstancesClient()

    # Get source disk
    disk = disk_client.get(project=project_id, zone=zone, disk=source_disk_name)

    for disk_user in disk.users:
        instance = instance_client.get(project=project_id, zone=zone, instance=disk_user)
        if instance.status in STOPPED_MACHINE_STATUS:
            continue
        if not force_create:
            raise RuntimeError(f"Instance {disk_user} should be stopped. For Windows instances please "
                               f"stop the instance using `GCESysprep` command. For Linux instances just "
                               f"shut it down normally. You can supress this error and create an image of"
                               f"the disk by setting `force_create` parameter to true (not recommended). \n"
                               f"More information here: \n"
                               f" * https://cloud.google.com/compute/docs/instances/windows/creating-windows-os-image#api \n"
                               f" * https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#prepare_instance_for_image")
        else:
            warnings.warn(f"Warning: The `force_create` option may compromise the integrity of your image. "
                          f"Stop the {disk_user} instance before you create the image if possible.")

    # Create image
    image = compute_v1.Image()
    image.source_disk = disk.self_link
    image.name = image_name
    if storage_location:
        image.storage_locations = [storage_location]

    operation = image_client.insert(project=project_id, image_resource=image)

    wait_for_extended_operation(operation, "image creation from disk")

    return image_client.get(project=project_id, image=image_name)
# </INGREDIENT>
