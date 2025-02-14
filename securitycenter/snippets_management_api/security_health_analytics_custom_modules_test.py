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
import os

import random

import time

import uuid

import backoff

from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable

from google.cloud import securitycentermanagement_v1

import pytest

import security_health_analytics_custom_modules

# Replace these variables before running the sample.
# GCLOUD_ORGANIZATION: The organization ID.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
LOCATION = "global"
PREFIX = "python_sample_sha_custom_module"

# Global list to track created shared modules
shared_modules = []


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    if not ORGANIZATION_ID:
        pytest.fail("GCLOUD_ORGANIZATION environment variable is not set.")

    setup_shared_modules()


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests(request):
    """Fixture to clean up created custom modules after the test session."""
    def teardown():
        print_all_shared_modules()
        cleanup_shared_modules()

    request.addfinalizer(teardown)


def setup_shared_modules():
    _, module_id = add_custom_module(ORGANIZATION_ID)
    if module_id != "" :
        shared_modules.append(module_id)


def add_module_to_cleanup(module_id):
    shared_modules.append(module_id)


def print_all_shared_modules():
    """Print all created custom modules."""
    if not shared_modules:
        print("No custom modules were created.")
    else:
        print("\nCreated Custom Modules:")
        for module_id in shared_modules:
            print(module_id)


def cleanup_shared_modules():
    """
    Deletes all created custom modules in this test session.
    """
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    print("Cleaning up created custom modules...")

    for module_id in list(shared_modules):
        if not custom_module_exists(module_id):
            print(f"Module not found (already deleted): {module_id}")
            shared_modules.remove(module_id)
            continue
        try:
            client.delete_security_health_analytics_custom_module(
                    request={"name": f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}/securityHealthAnalyticsCustomModules/{module_id}"}
                )
            print(f"Deleted custom module: {module_id}")
            shared_modules.remove(module_id)
        except Exception as e:
            print(f"Failed to delete module {module_id}: {e}")
            raise


def custom_module_exists(module_id):
    client = securitycentermanagement_v1.SecurityCenterManagementClient()
    try:
        client.get_security_health_analytics_custom_module(
                request={"name": f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}/securityHealthAnalyticsCustomModules/{module_id}"}
            )
        return True
    except Exception as e:
        if "404" in str(e):
            return False
        raise


def get_random_shared_module():
    if not shared_modules:
        return ""
    random.seed(int(time.time() * 1000000))
    return shared_modules[random.randint(0, len(shared_modules) - 1)]


def extract_custom_module_id(module_name):
    trimmed_full_name = module_name.strip()
    parts = trimmed_full_name.split("/")
    if parts:
        return parts[-1]
    return ""


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
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
    unique_suffix = str(uuid.uuid4()).replace("-", "_")
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
    module_id = extract_custom_module_id(module_name)
    return module_name, module_id


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_create_security_health_analytics_custom_module():
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Run the function to create the custom module
    response = security_health_analytics_custom_modules.create_security_health_analytics_custom_module(parent)
    add_module_to_cleanup(extract_custom_module_id(response.name))

    assert response is not None, "Custom module creation failed."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.SecurityHealthAnalyticsCustomModule.EnablementState.ENABLED


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_security_health_analytics_custom_module():

    module_id = get_random_shared_module()
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = security_health_analytics_custom_modules.get_security_health_analytics_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    assert response.display_name.startswith(PREFIX)
    response_org_id = response.name.split("/")[1]  # Extract organization ID from the name field
    assert response_org_id == ORGANIZATION_ID, f"Organization ID mismatch: Expected {ORGANIZATION_ID}, got {response_org_id}."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_delete_security_health_analytics_custom_module():

    module_id = get_random_shared_module()
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    try:
        response = security_health_analytics_custom_modules.delete_security_health_analytics_custom_module(parent, module_id)
    except Exception as e:
        pytest.fail(f"delete_security_health_analytics_custom_module() failed: {e}")
    assert response is None

    print(f"Custom module was deleted successfully: {module_id}")
    shared_modules.remove(module_id)


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_security_health_analytics_custom_module():

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the custom modules
    custom_modules = security_health_analytics_custom_modules.list_security_health_analytics_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_security_health_analytics_custom_module():

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    response = security_health_analytics_custom_modules.create_security_health_analytics_custom_module(parent)
    module_id = extract_custom_module_id(response.name)
    add_module_to_cleanup(module_id)

    # Retrieve the custom modules
    updated_custom_module = security_health_analytics_custom_modules.update_security_health_analytics_custom_module(parent, module_id)

    assert updated_custom_module is not None, "Failed to retrieve the updated custom module."
    response_org_id = updated_custom_module.name.split("/")[1]  # Extract organization ID from the name field
    assert response_org_id == ORGANIZATION_ID, f"Organization ID mismatch: Expected {ORGANIZATION_ID}, got {response_org_id}."
    assert updated_custom_module.enablement_state == securitycentermanagement_v1.SecurityHealthAnalyticsCustomModule.EnablementState.DISABLED


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_effective_security_health_analytics_custom_module():
    """Tests getting an effective SHA custom module."""
    module_id = get_random_shared_module()
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = security_health_analytics_custom_modules.get_effective_security_health_analytics_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    response_org_id = response.name.split("/")[1]  # Extract organization ID from the name field
    assert response_org_id == ORGANIZATION_ID, f"Organization ID mismatch: Expected {ORGANIZATION_ID}, got {response_org_id}."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_descendant_security_health_analytics_custom_module():
    """Tests listing descendant SHA custom modules."""
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the list descendant custom modules
    custom_modules = security_health_analytics_custom_modules.list_descendant_security_health_analytics_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_effective_security_health_analytics_custom_module():
    """Tests listing effective SHA custom modules."""
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the list of custom modules
    custom_modules = security_health_analytics_custom_modules.list_effective_security_health_analytics_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_simulate_security_health_analytics_custom_module():
    """Tests simulating an SHA custom module."""
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    simulated_custom_module = security_health_analytics_custom_modules.simulate_security_health_analytics_custom_module(parent)

    assert simulated_custom_module is not None, "Failed to retrieve the simulated custom module."
    assert simulated_custom_module.result.no_violation is not None, (
        f"Expected no_violation to be present, got {simulated_custom_module.result}."
    )
