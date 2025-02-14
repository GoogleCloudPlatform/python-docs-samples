#!/usr/bin/env python
#
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core.exceptions import GoogleAPICallError, NotFound, RetryError
from google.cloud import securitycentermanagement_v1


# [START securitycenter_get_effective_event_threat_detection_custom_module]
def get_effective_event_threat_detection_custom_module(parent: str, module_id: str):
    """
    Retrieves an Event Threat Detection custom module using parent and module id as parameters.
    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        The retrieved Event Threat Detection custom module.
    Raises:
        NotFound: If the specified custom module does not exist.
    """
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.GetEffectiveEventThreatDetectionCustomModuleRequest(
            name=f"{parent}/effectiveEventThreatDetectionCustomModules/{module_id}",
        )

        response = client.get_effective_event_threat_detection_custom_module(request=request)
        print(f"Retrieved Effective Event Threat Detection Custom Module: {response.name}")
        return response
    except NotFound as e:
        print(f"Custom Module not found: {e.message}")
        raise e
# [END securitycenter_get_effective_event_threat_detection_custom_module]


# [START securitycenter_list_effective_event_threat_detection_custom_module]
def list_effective_event_threat_detection_custom_module(parent: str):
    """
    Retrieves list of Event Threat Detection custom module.
    This includes resident modules defined at the scope of the parent,
    and inherited modules, inherited from ancestor organizations, folders, and projects (no descendants).

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        List of retrieved all Event Threat Detection custom modules.
    Raises:
        NotFound: If the parent resource is not found.
    """

    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.ListEffectiveEventThreatDetectionCustomModulesRequest(
            parent=parent,
        )

        response = client.list_effective_event_threat_detection_custom_modules(request=request)

        custom_modules = []
        for custom_module in response:
            print(f"Custom Module: {custom_module.name}")
            custom_modules.append(custom_module)
        return custom_modules
    except NotFound as e:
        print(f"Parent resource not found: {parent}")
        raise e
    except Exception as e:
        print(f"An error occurred while listing custom modules: {e}")
        raise e

# [END securitycenter_list_effective_event_threat_detection_custom_module]


# [START securitycenter_list_descendant_event_threat_detection_custom_module]
def list_descendant_event_threat_detection_custom_module(parent: str):
    """
    Retrieves list of all resident Event Threat Detection custom modules and all of its descendants.

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        List of retrieved all Event Threat Detection custom modules.
    Raises:
        NotFound: If the parent resource is not found.
    """

    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.ListDescendantEventThreatDetectionCustomModulesRequest(
            parent=parent,
        )

        response = client.list_descendant_event_threat_detection_custom_modules(request=request)

        custom_modules = []
        for custom_module in response:
            print(f"Custom Module: {custom_module.name}")
            custom_modules.append(custom_module)
        return custom_modules
    except NotFound as e:
        print(f"Parent resource not found: {parent}")
        raise e
    except Exception as e:
        print(f"An error occurred while listing custom modules: {e}")
        raise e

# [END securitycenter_list_descendant_event_threat_detection_custom_module]


# [START securitycenter_validate_event_threat_detection_custom_module]
def validate_event_threat_detection_custom_module(parent: str):
    """
    Validates a custom module for Event Threat Detection.

    Args:
        parent (str): Use any one of the following options:
            - organizations/{organization_id}/locations/{location_id}
            - folders/{folder_id}/locations/{location_id}
            - projects/{project_id}/locations/{location_id}
    """
    try:
        # Define the raw JSON configuration for the Event Threat Detection custom module
        raw_text = """
        {
            "ips": ["192.0.2.1"],
            "metadata": {
                "properties": {
                    "someProperty": "someValue"
                },
                "severity": "MEDIUM"
            }
        }
        """

        # Initialize the client
        client = securitycentermanagement_v1.SecurityCenterManagementClient()

        # Create the request
        request = securitycentermanagement_v1.ValidateEventThreatDetectionCustomModuleRequest(
            parent=parent,
            raw_text=raw_text,
            type="CONFIGURABLE_BAD_IP"
        )

        # Perform validation
        response = client.validate_event_threat_detection_custom_module(request=request)

        # Handle the response and output validation results
        if response.errors:
            print("Validation errors:")
            for error in response.errors:
                print(f"Field: {error.field_path}, Description: {error.description}")
            return response
        else:
            print("Validation successful: No errors found.")
            return response

    except GoogleAPICallError as api_error:
        print(f"API call failed: {api_error}")
    except RetryError as retry_error:
        print(f"Retry error occurred: {retry_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# [END securitycenter_validate_event_threat_detection_custom_module]
