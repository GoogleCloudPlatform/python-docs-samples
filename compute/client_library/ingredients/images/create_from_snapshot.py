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
from typing import Optional, Iterable

from google.cloud import compute_v1


# <INGREDIENT create_image_from_snapshot>
def create_image_from_snapshot(project_id: str, source_snapshot_name: str, image_name: str,
                               source_project_id: Optional[str] = None,
                               guest_os_features: Optional[Iterable[str]] = None,
                               storage_location: Optional[str] = None) -> compute_v1.Image:
    """
    Creates an image based on a snapshot.

    Args:
        project_id: project ID or project number of the Cloud project you want to place your new image in.
        source_snapshot_name: name of the snapshot you want to use as a base of your image.
        image_name: name of the image you want to create.
        source_project_id: name of the project that hosts the source snapshot. If left unset, it's assumed to equal
            the `project_id`.
        guest_os_features: an iterable collection of guest features you want to enable for the bootable image.
            Learn more about Guest OS features here:
            https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features
        storage_location: the storage location of your image. For example, specify "us" to store the image in the
            `us` multi-region, or "us-central1" to store it in the `us-central1` region. If you do not make a selection,
             Compute Engine stores the image in the multi-region closest to your image's source location.

    Returns:
        An Image object.
    """
    if source_project_id is None:
        source_project_id = project_id

    snapshot_client = compute_v1.SnapshotsClient()
    image_client = compute_v1.ImagesClient()
    src_snapshot = snapshot_client.get(project=source_project_id, snapshot=source_snapshot_name)

    image = compute_v1.Image()
    image.name = image_name
    image.source_snapshot = src_snapshot.self_link

    if storage_location:
        image.storage_locations = [storage_location]

    if guest_os_features:
        image.guest_os_features = [compute_v1.GuestOsFeature(type_=feature) for feature in guest_os_features]

    operation = image_client.insert(project=project_id, image_resource=image)

    wait_for_extended_operation(operation, "image creation from snapshot")

    return image_client.get(project=project_id, image=image_name)
# </INGREDIENT>
