#  Copyright 2024 Google LLC
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


# <INGREDIENT delete_regional_instance_template>
def delete_regional_instance_template(
    project_id: str, region: str, template_name: str
) -> None:
    """Deletes a regional instance template in Google Cloud.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the instance template is located.
        template_name (str): The name of the instance template to delete.
    Returns:
        None
    """
    client = compute_v1.RegionInstanceTemplatesClient()

    operation = client.delete(
        project=project_id, region=region, instance_template=template_name
    )
    wait_for_extended_operation(operation, "Instance template deletion")


# </INGREDIENT>
