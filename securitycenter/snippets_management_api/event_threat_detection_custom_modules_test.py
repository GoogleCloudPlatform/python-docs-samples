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

from google.protobuf.struct_pb2 import Struct

import pytest

import event_threat_detection_custom_modules

# Replace these variables before running the sample.
# GCLOUD_ORGANIZATION: The organization ID.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
LOCATION = "global"
PREFIX = "python_sample_etd_custom_module"  # Prefix used for identifying test modules


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Fixture to ensure a clean environment by removing test modules before running tests."""
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
        custom_modules = client.list_event_threat_detection_custom_modules(
            request={"parent": parent}
        )
        for module in custom_modules:
            if module.display_name.startswith(PREFIX):
                client.delete_event_threat_detection_custom_module(
                    request={"name": module.name}
                )
                print(f"Deleted custom module: {module.name}")
    except NotFound as e:
        print(f"Resource not found: {e}")
    except Exception as e:
        print(f"Unexpected error during cleanup: {e}")
        raise


def add_custom_module(org_id: str):

    parent = f"organizations/{org_id}/locations/global"
    client = securitycentermanagement_v1.SecurityCenterManagementClient()

    # Generate a unique display name
    unique_suffix = f"{int(time.time())}_{random.randint(0, 999)}"
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
    module_id = module_name.split("/")[-1]
    return module_name, module_id


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_create_event_threat_detection_custom_module():
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Run the function to create the custom module
    response = event_threat_detection_custom_modules.create_event_threat_detection_custom_module(parent)

    assert response is not None, "Custom module creation failed."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.EventThreatDetectionCustomModule.EnablementState.ENABLED


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_event_threat_detection_custom_module():

    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = event_threat_detection_custom_modules.get_event_threat_detection_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.EventThreatDetectionCustomModule.EnablementState.ENABLED
    print(f"Retrieved Custom Module: {response.name}")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_event_threat_detection_custom_module():

    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the custom modules
    custom_modules = event_threat_detection_custom_modules.list_event_threat_detection_custom_module(parent)

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
        == securitycentermanagement_v1.EventThreatDetectionCustomModule.EnablementState.ENABLED
    )


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_event_threat_detection_custom_module():

    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the custom module
    response = event_threat_detection_custom_modules.update_event_threat_detection_custom_module(parent, module_id)

    assert response is not None, "Failed to retrieve the custom module."
    # Verify that the custom module was created
    assert response.display_name.startswith(PREFIX)
    assert response.enablement_state == securitycentermanagement_v1.EventThreatDetectionCustomModule.EnablementState.DISABLED


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_delete_event_threat_detection_custom_module():

    module_name, module_id = add_custom_module(ORGANIZATION_ID)
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    try:
        response = event_threat_detection_custom_modules.delete_event_threat_detection_custom_module(parent, module_id)
    except Exception as e:
        pytest.fail(f"delete_event_threat_detection_custom_module() failed: {e}")
        return
    assert response is None

    print(f"Custom module was deleted successfully: {module_id}")
