#!/usr/bin/env python
#
# Copyright 2024 Google LLC
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

from google.api_core.exceptions import NotFound
from google.cloud import securitycentermanagement_v1

# [START securitycenter_get_effective_security_health_analytics_custom_module]


def get_effective_security_health_analytics_custom_module(parent: str, module_id: str):
    """
    Retrieves a Security Health Analytics custom module.
    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        The retrieved Security Health Analytics custom module.
    Raises:
        NotFound: If the specified custom module does not exist.
    """
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(
            name=f"{parent}/effectiveSecurityHealthAnalyticsCustomModules/{module_id}",
        )

        response = client.get_effective_security_health_analytics_custom_module(request=request)
        print(f"Retrieved Effective Security Health Analytics Custom Module: {response.name}")
        return response
    except NotFound as e:
        print(f"Custom Module not found: {response.name}")
        raise e
# [END securitycenter_get_effective_security_health_analytics_custom_module]

# [START securitycenter_list_descendant_security_health_analytics_custom_module]


def list_descendant_security_health_analytics_custom_module(parent: str):
    """
    Retrieves list of all resident Security Health Analytics custom modules and all of its descendants.
    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        List of retrieved all resident Security Health Analytics custom modules and all of its descendants.
    Raises:
        NotFound: If the specified custom module does not exist.
    """

    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.ListDescendantSecurityHealthAnalyticsCustomModulesRequest(
            parent=parent,
        )

        response = client.list_descendant_security_health_analytics_custom_modules(request=request)

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
# [END securitycenter_list_descendant_security_health_analytics_custom_module]

# [START securitycenter_list_effective_security_health_analytics_custom_module]


def list_effective_security_health_analytics_custom_module(parent: str):
    """
    Retrieves list of all Security Health Analytics custom modules.
    This includes resident modules defined at the scope of the parent,
    and inherited modules, inherited from ancestor organizations, folders, and projects (no descendants).

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        List of retrieved all Security Health Analytics custom modules.
    Raises:
        NotFound: If the specified custom module does not exist.
    """

    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    try:
        request = securitycentermanagement_v1.ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(
            parent=parent,
        )

        response = client.list_effective_security_health_analytics_custom_modules(request=request)

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
# [END securitycenter_list_effective_security_health_analytics_custom_module]

# [START securitycenter_simulate_security_health_analytics_custom_module]


def simulate_security_health_analytics_custom_module(parent: str):
    """
    Simulates the result of using a SecurityHealthAnalyticsCustomModule to check a resource.

    Args:
        parent: Use any one of the following options:
                - organizations/{organization_id}/locations/{location_id}
                - folders/{folder_id}/locations/{location_id}
                - projects/{project_id}/locations/{location_id}
    Returns:
        Simulated Security Health Analytics custom module.
    """

    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    # Define the custom config configuration
    custom_config = {
        "description": (
            "Sample custom module for testing purposes. This custom module evaluates "
            "Cloud KMS CryptoKeys to ensure their rotation period exceeds 30 days (2592000 seconds)."
        ),
        "predicate": {
            "expression": "has(resource.rotationPeriod) && (resource.rotationPeriod > duration('2592000s'))",
            "title": "Cloud KMS CryptoKey Rotation Period",
            "description": (
                "Evaluates whether the rotation period of a Cloud KMS CryptoKey exceeds 30 days. "
                "A longer rotation period might increase the risk of exposure."
            ),
        },
        "recommendation": (
            "Review and adjust the rotation period for Cloud KMS CryptoKeys to align with your security policies. "
            "Consider setting a shorter rotation period if possible."
        ),
        "resource_selector": {"resource_types": ["cloudkms.googleapis.com/CryptoKey"]},
        "severity": "CRITICAL",
        "custom_output": {
            "properties": [
                {
                    "name": "example_property",
                    "value_expression": {
                        "description": "The resource name of the CryptoKey being evaluated.",
                        "expression": "resource.name",
                        "location": "global",
                        "title": "CryptoKey Resource Name",
                    },
                }
            ]
        },
    }

    # Initialize request argument(s)
    resource = securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource()
    resource.resource_type = "cloudkms.googleapis.com/CryptoKey"  # Replace with the correct resource type

    request = securitycentermanagement_v1.SimulateSecurityHealthAnalyticsCustomModuleRequest(
        parent=parent,
        custom_config=custom_config,
        resource=resource,
    )

    response = client.simulate_security_health_analytics_custom_module(request=request)

    print(f"Simulated Security Health Analytics Custom Module: {response}")
    return response

# [END securitycenter_simulate_security_health_analytics_custom_module]
