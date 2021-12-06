# Copyright 2021 Google LLC
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

from typing import Iterable

# [START compute_images_get]
# [START compute_images_get_list]
from google.cloud import compute_v1

# [END compute_images_get_list]
# [END compute_images_get]


# [START compute_images_get_list]
def list_images(project_id: str) -> Iterable[compute_v1.Image]:
    """
    Retrieve a list of images available in given project.

    Args:
        project_id: project ID or project number of the Cloud project you want to list images from.

    Returns:
        An iterable collection of compute_v1.Image objects.
    """
    image_client = compute_v1.ImagesClient()
    return image_client.list(project=project_id)


# [END compute_images_get_list]


# [START compute_images_get]
def get_image(project_id: str, image_name: str) -> compute_v1.Image:
    """
    Retrieve detailed information about a single image from a project.

    Args:
        project_id: project ID or project number of the Cloud project you want to list images from.
        image_name: name of the image you want to get details of.

    Returns:
        An instance of compute_v1.Image object with information about specified image.
    """
    image_client = compute_v1.ImagesClient()
    return image_client.get(project=project_id, image=image_name)


# [END compute_images_get]
