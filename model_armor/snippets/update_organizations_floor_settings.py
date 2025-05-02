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
Sample code for updating the model armor floor settings of an organization.
"""

from google.cloud import modelarmor_v1


def update_organization_floor_settings(
    organization_id: str,
) -> modelarmor_v1.FloorSetting:
    """Update floor settings of an organization.

    Args:
        organization_id (str): Google Cloud organization ID for which floor
            settings need to be updated.

    Returns:
        FloorSetting: Updated organization floor settings.
    """
    # [START modelarmor_update_organization_floor_settings]

    from google.cloud import modelarmor_v1

    # Create the Model Armor client.
    client = modelarmor_v1.ModelArmorClient(transport="rest")

    # TODO (Developer): Uncomment these variables and initialize
    # organization_id = "YOUR_ORGANIZATION_ID"

    # Prepare organization floor setting path/name
    floor_settings_name = (
        f"organizations/{organization_id}/locations/global/floorSetting"
    )

    # Update the organization floor setting
    # For more details on filters, please refer to the following doc:
    # https://cloud.google.com/security-command-center/docs/key-concepts-model-armor#ma-filters
    response = client.update_floor_setting(
        request=modelarmor_v1.UpdateFloorSettingRequest(
            floor_setting=modelarmor_v1.FloorSetting(
                name=floor_settings_name,
                filter_config=modelarmor_v1.FilterConfig(
                    rai_settings=modelarmor_v1.RaiFilterSettings(
                        rai_filters=[
                            modelarmor_v1.RaiFilterSettings.RaiFilter(
                                filter_type=modelarmor_v1.RaiFilterType.HATE_SPEECH,
                                confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                            )
                        ]
                    ),
                ),
                enable_floor_setting_enforcement=True,
            )
        )
    )
    # Print the updated config
    print(response)

    # [END modelarmor_update_organization_floor_settings]

    return response
