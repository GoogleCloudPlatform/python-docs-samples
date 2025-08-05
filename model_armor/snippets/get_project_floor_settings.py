# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Sample code for getting floor settings of a project.
"""

from google.cloud import modelarmor_v1


def get_project_floor_settings(project_id: str) -> modelarmor_v1.FloorSetting:
    """Get details of a single floor setting of a project.

    Args:
        project_id (str): Google Cloud project ID to retrieve floor settings.

    Returns:
        FloorSetting: Floor setting for the specified project.
    """
    # [START modelarmor_get_project_floor_settings]

    from google.cloud import modelarmor_v1

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(transport="rest")

    # TODO(Developer): Uncomment below variable.
    # project_id = "YOUR_PROJECT_ID"

    floor_settings_name = f"projects/{project_id}/locations/global/floorSetting"

    # Get the project floor setting.
    response = client.get_floor_setting(
        request=modelarmor_v1.GetFloorSettingRequest(name=floor_settings_name)
    )

    # Print the retrieved floor setting.
    print(response)

    # [END modelarmor_get_project_floor_settings]

    return response
