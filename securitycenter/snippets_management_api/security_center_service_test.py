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

import backoff

from google.api_core.exceptions import InternalServerError, NotFound, ServiceUnavailable

import pytest

import security_center_service

# Replace these variables before running the sample.
# GCLOUD_ORGANIZATION: The organization ID.
ORGANIZATION_ID = os.environ["GCLOUD_ORGANIZATION"]
LOCATION = "global"


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    if not ORGANIZATION_ID:
        pytest.fail("GCLOUD_ORGANIZATION environment variable is not set.")


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_get_security_center_service():

    service = "event-threat-detection"
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"

    # Retrieve the security center service
    response = security_center_service.get_security_center_service(parent, service)

    assert response is not None, "Failed to retrieve the SecurityCenterService."
    assert service in response.name, f"Expected service ID {service} in response, got {response.name}."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_list_security_center_service():

    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Retrieve the list of security center services
    response = security_center_service.list_security_center_service(parent)

    assert response is not None, "Failed to list Security Center services."
    assert len(response) > 0, "No Security Center services were retrieved."
    assert any(ORGANIZATION_ID in service.name for service in response), \
        f"Expected organization ID {ORGANIZATION_ID} in one of the services, but none were found."


@backoff.on_exception(
    backoff.expo, (InternalServerError, ServiceUnavailable, NotFound), max_tries=3
)
def test_update_security_center_service():

    service = "event-threat-detection"
    parent = f"organizations/{ORGANIZATION_ID}/locations/{LOCATION}"
    # Update the security center service
    updated_service = security_center_service.update_security_center_service(parent, service)

    assert updated_service is not None, "Failed to retrieve the Security Center service."
    assert ORGANIZATION_ID in updated_service.name, \
        f"Expected organization ID {ORGANIZATION_ID} in the updated service, got {updated_service.name}."
    assert service in updated_service.name, f"Expected service ID {service} in updated service, got {updated_service.name}."
    assert updated_service.intended_enablement_state.name == "DISABLED", \
        f"Expected enablement state to be 'DISABLED', got {updated_service.intended_enablement_state.name}."
