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

from google.protobuf.struct_pb2 import Struct

import pytest

import event_threat_detection_custom_modules

# Replace these variables before running the sample.
# GCLOUD_ORGANIZATION: The organization ID.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
LOCATION = "global"
PREFIX = "python_sample_etd_custom_module"

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
    for _ in range(3) :
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
            client.delete_event_threat_detection_custom_module(
                    request={"name": f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}/eventThreatDetectionCustomModules/{module_id}"}
                )
            print(f"Deleted custom module: {module_id}")
            shared_modules.remove(module_id)
        except Exception as e:
            print(f"Failed to delete module {module_id}: {e}")
            raise


def custom_module_exists(module_id):
    client = securitycentermanagement_v1.SecurityCenterManagementClient()
    try:
        client.get_event_threat_detection_custom_module(
                request={"name": f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}/eventThreatDetectionCustomModules/{module_id}"}
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


def add_custom_module(org_id: str):

    parent = f"organizations/{org_id}/locations/global"
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    # Generate a unique display name
    unique_suffix = str(uuid.uuid4()).replace("-", "_")
    display_name = f"python_sample_etd_custom_module_test_{unique_suffix}"

    # Define the metadata and other config parameters as a dictionary
    config_map = {
        "metadata": {
            "severity": "MEDIUM",
            "description": "Sample custom module for testing purposes. Please do not delete.",
            "recommendation": "na",
        },
        "ips": ["0.0.0.0"],
    }

    # Convert the dictionary to a Struct
    config_struct = Struct()
    config_struct.update(config_map)

    # Define the custom module configuration
    custom_module = {
        "display_name": display_name,
        "enablement_state": "ENABLED",
        "type_": "CONFIGURABLE_BAD_IP",
        "config": config_struct,
    }

    request = securitycentermanagement_v1.CreateEventThreatDetectionCustomModuleRequest(
        parent=parent,
        event_threat_detection_custom_module=custom_module,
    )
    response = client.create_event_threat_detection_custom_module(request=request)
    print(f"Created Event Threat Detection Custom Module: {response.name}")
    module_name = response.name
    module_id = extract_custom_module_id(module_name)
    return module_name, module_id


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_effective_event_threat_detection_custom_module():

    module_id = get_random_shared_module()
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = event_threat_detection_custom_modules.get_effective_event_threat_detection_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_effective_event_threat_detection_custom_module():

    module_id = get_random_shared_module()

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the custom modules
    custom_modules = event_threat_detection_custom_modules.list_effective_event_threat_detection_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."

    # Verify the created module is in the list
    created_module = next(
        (module for module in custom_modules if extract_custom_module_id(module.name) == module_id), None
    )
    assert created_module is not None, "Created custom module not found in the list."
    assert created_module.display_name.startswith(PREFIX)
    assert (
        created_module.enablement_state
        == securitycentermanagement_v1.EffectiveEventThreatDetectionCustomModule.EnablementState.ENABLED
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_descendant_event_threat_detection_custom_module():

    module_id = get_random_shared_module()

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the custom modules
    custom_modules = event_threat_detection_custom_modules.list_descendant_event_threat_detection_custom_module(parent)

    assert custom_modules is not None, "Failed to retrieve the custom modules."
    assert len(custom_modules) > 0, "No custom modules were retrieved."

    # Verify the created module is in the list
    created_module = next(
        (module for module in custom_modules if extract_custom_module_id(module.name) == module_id), None
    )
    assert created_module is not None, "Created custom module not found in the list."
    assert created_module.display_name.startswith(PREFIX)
    assert (
        created_module.enablement_state
        == securitycentermanagement_v1.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_validate_event_threat_detection_custom_module():

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = event_threat_detection_custom_modules.validate_event_threat_detection_custom_module(parent)

    assert response is not None, "Failed to retrieve the validte ETD custom module response."
