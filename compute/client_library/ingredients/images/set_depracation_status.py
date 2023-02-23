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


# <INGREDIENT set_deprecation_status>
def set_deprecation_status(project_id: str, image_name: str, status: compute_v1.DeprecationStatus.State) -> None:
    """
    Modify the deprecation status of an image.

    Note: Image objects by default don't have the `deprecated` attribute at all unless it's set.

    Args:
        project_id: project ID or project number of the Cloud project that hosts the image.
        image_name: name of the image you want to modify
        status: the status you want to set for the image. Available values are available in
            `compute_v1.DeprecationStatus.State` enum. Learn more about image deprecation statuses:
            https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#deprecation-states
    """
    image_client = compute_v1.ImagesClient()
    deprecation_status = compute_v1.DeprecationStatus()
    deprecation_status.state = status.name
    operation = image_client.deprecate(project=project_id, image=image_name,
                                       deprecation_status_resource=deprecation_status)

    wait_for_extended_operation(operation, "changing deprecation state of an image")
# </INGREDIENT>
