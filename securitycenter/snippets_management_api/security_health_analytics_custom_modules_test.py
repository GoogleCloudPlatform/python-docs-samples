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
import os

import random

import time

import backoff

from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable

from google.cloud import securitycentermanagement_v1

import pytest

import security_health_analytics_custom_modules

# Replace these variables before running the sample.
# GCLOUD_ORGANIZATION: The organization ID.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
LOCATION = "global"
PREFIX = "python_sample_sha_custom_module"  # Prefix used for identifying test modules


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """
    Fixture to ensure a clean environment by removing test modules before running tests.

    This fixture lists all SHA custom modules in the organization and deletes any
    that were created by previous test runs, identified by the PREFIX.
    """
    if not ORGANIZATION_ID:
        pytest.fail("GCLOUD_ORGANIZATION environment variable is not set.")

    print(f"Cleaning up existing custom modules for organization: {ORGANIZATION_ID}")
    cleanup_existing_custom_modules(ORGANIZATION_ID)


def cleanup_existing_custom_modules(org_id: str):
    """
    Deletes all custom modules matching a specific naming pattern.
    Args:
        org_id: The organization ID.
    """
    client = securitycentermanagement_v1.SecurityCenterManagementClient()
    parent = f"organizations/{org_id}/locations/global"
    print(f"Parent path: {parent}")
    try:
        custom_modules = client.list_security_health_analytics_custom_modules(
            request={"parent": parent}
        )
        for module in custom_modules:
            if module.display_name.startswith(PREFIX):
                client.delete_security_health_analytics_custom_module(
                    request={"name": module.name}
                )
                print(f"Deleted custom module: {module.name}")
    except NotFound as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Unexpected error during cleanup: {e}")
        raise


def add_custom_module(org_id: str):
    """
    Adds a new SHA custom module.
    Args:
        org_id (str): The organization ID.
    Returns:
        Tuple[str, str]: The name and ID of the created custom module.
    """
    parent = f"organizations/{org_id}/locations/global"
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    # Generate a unique display name
    unique_suffix = f"{int(time.time())}_{random.randint(0, 999)}"
    display_name = f"python_sample_sha_custom_module_test_{unique_suffix}"

    # Define the custom module configuration
    custom_module = {
        "display_name": display_name,
        "enablement_state": "ENABLED",
        "custom_config": {
            "description": "Sample custom module for testing purposes. Please do not delete.",
            "predicate": {
                "expression": "has(resource.rotationPeriod) && (resource.rotationPeriod > duration('2592000s'))",
                "title": "Cloud KMS CryptoKey Rotation Period",
                "description": "Custom module to detect CryptoKeys with rotation period greater than 30 days.",
            },
            "recommendation": "Review and adjust the rotation period for Cloud KMS CryptoKeys.",
            "resource_selector": {"resource_types": ["cloudkms.googleapis.com/CryptoKey"]},
            "severity": "CRITICAL",
            "custom_output": {
                "properties": [
                    {
                        "name": "example_property",
                        "value_expression": {
                            "description": "The resource name of the CryptoKey",
                            "expression": "resource.name",
                            "location": "global",
                            "title": "CryptoKey Resource Name",
                        },
                    }
                ]
            },
        },
    }

    request = securitycentermanagement_v1.CreateSecurityHealthAnalyticsCustomModuleRequest(
        parent=parent,
        security_health_analytics_custom_module=custom_module,
    )
    response = client.create_security_health_analytics_custom_module(request=request)
    print(f"Created Security Health Analytics Custom Module: {response.name}")
    module_name = response.name
    module_id = module_name.split("/")[-1]
    return module_name, module_id


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_effective_security_health_analytics_custom_module():
    """Tests getting an effective SHA custom module."""
    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = security_health_analytics_custom_modules.get_effective_security_health_analytics_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    print(f"Retrieved Custom Module: {response.name}")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_descendant_security_health_analytics_custom_module():
    """Tests listing descendant SHA custom modules."""
    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the list descendant custom modules
    custom_modules = security_health_analytics_custom_modules.list_descendant_security_health_analytics_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."

    # Verify the created module is in the list
    created_module = next(
        (module for module in custom_modules if module.name == module_name), None
    )
    assert created_module is not None, "Created custom module not found in the list."
    assert created_module.display_name.startswith(PREFIX)
    assert (
        created_module.enablement_state
        == securitycentermanagement_v1.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_effective_security_health_analytics_custom_module():
    """Tests listing effective SHA custom modules."""
    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the list of custom modules
    custom_modules = security_health_analytics_custom_modules.list_effective_security_health_analytics_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."

    # Verify the created module is in the list
    created_module = next(
        (module for module in custom_modules if (module.name.split("/")[-1]) == module_id), None
    )
    assert created_module is not None, "Created custom module not found in the list."
    assert created_module.display_name.startswith(PREFIX)
    assert (
        created_module.enablement_state
        == securitycentermanagement_v1.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState.ENABLED
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_simulate_security_health_analytics_custom_module():
    """Tests simulating an SHA custom module."""
    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    simulated_custom_module = security_health_analytics_custom_modules.simulate_security_health_analytics_custom_module(parent)

    assert simulated_custom_module is not None, "Failed to retrieve the simulated custom module."
    assert simulated_custom_module.result.no_violation is not None, (
        f"Expected no_violation to be present, got {simulated_custom_module.result}."
    )
