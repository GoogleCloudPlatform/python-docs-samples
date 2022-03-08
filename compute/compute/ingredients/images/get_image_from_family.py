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


# <INGREDIENT get_image_from_family>
def get_image_from_family(project: str, family: str) -> compute_v1.Image:
    """
    Retrieve the newest image that is part of a given family in a project.

    Args:
        project: project ID or project number of the Cloud project you want to get image from.
        family: name of the image family you want to get image from.

    Returns:
        An Image object.
    """
    image_client = compute_v1.ImagesClient()
    # List of public operating system (OS) images: https://cloud.google.com/compute/docs/images/os-details
    newest_image = image_client.get_from_family(
        project=project, family=family
    )
    return newest_image
# </INGREDIENT>
